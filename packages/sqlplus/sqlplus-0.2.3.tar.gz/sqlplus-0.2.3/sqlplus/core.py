"""
sqlite3 based utils for statistical analysis

reeling off rows from db(sqlite3) and saving them back to db
"""
import os
import re
import sqlite3
import copy
import warnings
import inspect
import operator
import numpy as np
import csv
import statistics as st
import pandas as pd

from sas7bdat import SAS7BDAT
from scipy.stats import ttest_1samp
from collections import OrderedDict
from contextlib import contextmanager
from itertools import groupby, islice, chain, tee, \
    zip_longest, accumulate
from pypred import Predicate

from .util import isnum, listify, peek_first, \
    parse_model, random_string, ymd, star

# pandas raises warnings because maintainers of statsmodels are lazy
warnings.filterwarnings('ignore')
import statsmodels.api as sm


WORKSPACE = ''


@contextmanager
def dbopen(dbfile, cache_size=100000, temp_store=2):
    # temp_store might be deprecated
    "Connects to SQL database(sqlite)"
    splus = SQLPlus(dbfile, cache_size, temp_store)
    try:
        yield splus
    finally:
        # should I close the cursor?
        splus._cursor.close()
        splus.conn.commit()
        splus.conn.close()


# aggreate function builder
class AggBuilder:
    def __init__(self):
        self.rows = []

    def step(self, *args):
        self.rows.append(args)


# Don't try to be smart, unless you really know well
class Row:
    "mutable version of sqlite3.row"
    # works for python 3.6 and higher
    def __init__(self, **kwargs):
        super().__setattr__('_ordered_dict', OrderedDict(**kwargs))

    def copy(self):
        r = Row()
        for c, v in zip(self.columns, self.values):
            r[c] = v
        return r

    @property
    def columns(self):
        return list(self._ordered_dict.keys())

    @property
    def values(self):
        return list(self._ordered_dict.values())

    def __getattr__(self, name):
        return self._ordered_dict[name]

    def __setattr__(self, name, value):
        self._ordered_dict[name] = value

    def __delattr__(self, name):
        del self._ordered_dict[name]

    def __getitem__(self, name):
        return self._ordered_dict[name]

    def __setitem__(self, name, value):
        self._ordered_dict[name] = value

    def __delitem__(self, name):
        del self._ordered_dict[name]

    def __repr__(self):
        content = ', '.join(c + '=' + repr(v) for c, v in
                            zip(self.columns, self.values))
        return 'Row(' + content + ')'

    # for pickling, very important
    def __getstate__(self):
        return self.__dict__

    def __setstate__(self, d):
        self.__dict__.update(d)

    # TODO:
    # hasattr doesn't work properly
    # you can't make it work by changing getters and setters
    # to an ordinary way. but it is slower


class Rows:
    """
    a shallow wrapper of a list of row instances """
    # don't try to define __getattr__, __setattr__
    # list objects has a lot of useful attributes that can't be overwritten
    # not the same situation as 'row' class

    # inheriting list can be problemetic
    # when you want to use this as a superclass
    # see 'where' method, you must return 'self' but it's not efficient
    # (at least afaik) if you inherit list

    def __init__(self, rows):
        self.rows = list(rows)

    def __len__(self):
        return len(self.rows)

    # __getitem__ enables you to iterate 'Rows'
    def __getitem__(self, k):
        "cols: integer or list of strings or comma separated string"
        if isinstance(k, int):
            return self.rows[k]
        if isinstance(k, slice):
            # shallow copy for non-destructive slicing
            return self._newrows(self.rows[k])
        # Now k is a column name(s)
        k = listify(k)
        if len(k) == 1:
            k = k[0]
            return [r[k] for r in self.rows]
        else:
            # exceptionally allow multiple columns for __getitem__
            return [[r[k1] for k1 in k] for r in self.rows]

    def __setitem__(self, k, v):
        if isinstance(k, int) or isinstance(k, slice):
            self.rows[k] = v
            return

        # same value is assigned to them all
        if not isinstance(v, list):
            for r in self.rows:
                r[k] = v
        else:
            assert len(self) == len(v), "Invalid assignment"
            for r, v1 in zip(self.rows, v):
                r[k] = v1

    def __delitem__(self, k):
        if isinstance(k, int) or isinstance(k, slice):
            del self.rows[k]
            return

        for r in self.rows:
            del r[k]

    def __add__(self, other):
        return self._newrows(self.rows + other.rows)

    # You can write a function that sort of fills in missing date rows
    # zipping like left join, based on column
    # I thought this could be useful...
    def lzip(self, col, *rss):
        """self and rss are all ordered(ascending) and
        none of them contains dups
        Parameters:
            rss: a list of a sequence of instances of 'Row',
                a sequence can be either a list of iterator
        """
        # This should be fast, so the verification steps are ignored
        rss = [iter(rs) for rs in rss]

        def gen(rs0, rs1):
            doneflag = False
            try:
                r1 = next(rs1)
            except:
                doneflag = True

            for r0 in rs0:
                if doneflag:
                    yield None
                    continue
                v0, v1 = r0[col], r1[col]
                if v0 < v1:
                    yield None
                    continue
                elif v0 == v1:
                    yield r1
                    try:
                        r1 = next(rs1)
                    except:
                        doneflag = True
                else:
                    while v0 > v1:
                        try:
                            # throw away
                            r1 = next(rs1)
                            v1 = r1[col]
                        except:
                            doneflag = True
                            break
                        # nothing to yield
                    if v0 == v1:
                        yield r1
                    # passed over
                    else:
                        yield None

        rs0s = tee(iter(self), len(rss) + 1)
        seqs = (gen(rs0, rs1) for rs0, rs1 in zip(rs0s[1:], rss))
        yield from zip(rs0s[0], *seqs)

    def isconsec(self, col, step, fmt):
        for x1, x2 in zip(self, self[1:]):
            if ymd(x1[col], step, fmt) != x2[col]:
                return False
        return True

    def roll(self, size=None, step=None, col=None, nextfn=None):
        "group rows over time, allowing overlaps"
        self.order(col)
        for ls in _roll(self.rows, size, step, _build_keyfn(col), nextfn):
            yield self._newrows(ls)

    # destructive!!!
    def order(self, key, reverse=False):
        # You can pass fn as key arg but not recommended
        self.rows.sort(key=_build_keyfn(key), reverse=reverse)
        return self

    def copy(self):
        "shallow copy"
        # I'm considering the inheritance
        return copy.copy(self)

    def _newrows(self, rs):
        # copying rows and build Rows object
        # Am I worring too much?, this is for inheritance
        self.rows, temp = [], self.rows
        other = self.copy()
        other.rows, self.rows = list(rs), temp
        return other

    def where(self, pred):
        if isinstance(pred, str):
            obj = Predicate(pred)
            return self._newrows([r for r in self
                                  if obj.evaluate(r._ordered_dict)])
        return self._newrows([r for r in self if pred(r)])

    def isnum(self, *cols):
        "another simplified filtering, numbers only"
        cols = listify(','.join(cols))
        return self._newrows([r for r in self if isnum(*(r[c] for c in cols))])

    # Won't be used often
    def istext(self, *cols):
        "another simplified filtering, texts(string) only"
        cols = listify(','.join(cols))
        return self._newrows([r for r in self
                              if all(isinstance(r[c], str) for c in cols)])

    def avg(self, col, wcol=None, n=None):
        # wcol: column for weight,
        # n: you may want to round up
        if wcol:
            rs = self.isnum(col, wcol)
            total = sum(r[wcol] for r in rs)
            val = sum(r[col] * r[wcol] for r in rs) / total
        else:
            val = st.mean(r[col] for r in self if isnum(r[col]))
        return round(val, n) if n else val

    # Simple one but..
    def ols(self, model):
        y, *xs = parse_model(model)
        X = [[r[x] for x in xs] for r in self]
        res = sm.OLS(self[y], sm.add_constant(X)).fit()
        return res

    def truncate(self, col, limit=0.01):
        "Truncate extreme values, defalut 1 percent on both sides"
        xs = self[col]
        lower = np.percentile(xs, limit * 100)
        higher = np.percentile(xs, (1 - limit) * 100)
        self.rows = self.where(lambda r: r[col] >= lower and r[col] <= higher)\
                        .rows
        return self

    def winsorize(self, col, limit=0.01):
        xs = self[col]
        lower = np.percentile(xs, limit * 100)
        higher = np.percentile(xs, (1 - limit) * 100)
        for r in self.rows:
            if r[col] > higher:
                r[col] = higher
            elif r[col] < lower:
                r[col] = lower
        return self

    # implicit ordering
    def group(self, key):
        # key can be a fn but not recommended
        keyfn = _build_keyfn(key)
        for _, rs in groupby(self.order(keyfn), keyfn):
            yield self._newrows(list(rs))

    def chunks(self, n, col=None, le=True):
        size = len(self)
        if isinstance(n, int):
            start = 0
            for i in range(1, n + 1):
                end = int((size * i) / n)
                # must yield anyway
                try:
                    val = self[start:end]
                except:
                    val = self._newrows([])
                yield val
                start = end
        # n is a list of percentiles
        elif not col:
            # then it is a list of percentiles for each chunk
            assert sum(n) <= 1, f"Sum of percentils for chunks must be <= 1.0"
            ns = [int(x * size) for x in accumulate(n)]
            for a, b in zip([0] + ns, ns):
                yield self[a:b]
        # n is a list of break points
        else:
            self.order(col)
            size = len(self)
            op = operator.le if le else operator.lt
            start, end = 0, 0
            for bp in n:
                while op(self[end][col], bp) and end < size:
                    end += 1
                yield self[start:end]
                start = end
            yield self[end:]

    def bps(self, percentiles, col):
        "Breakpoints from percentages"
        bs = pd.Series(self[col]).describe(percentiles)
        return [bs[str(round(p * 100)) + '%'] for p in percentiles]

    # Use this when you need to see what's inside
    # for example, when you want to see the distribution of data.
    def df(self, cols=None):
        if cols:
            cols = listify(cols)
            return pd.DataFrame([[r[col] for col in cols] for r in self.rows],
                                columns=cols)
        else:
            cols = self.rows[0].columns
            seq = _safe_values(self.rows, cols)
            return pd.DataFrame(list(seq), columns=cols)

    # Only for debugging
    def show(self):
        print(self.df())

    def ttest(self, col, n=3, popmean=0.0):
        "simplified rep of tstat"
        seq = self[col]
        _, pval = ttest_1samp(seq, popmean)
        return star(st.mean(seq), pval, n=n)

    def numbering(self, d, dep=False, prefix='pn_'):
        "d: {'col1': 3, 'col2': [0.3, 0.4, 0.3], 'col3': fn}"
        d1 = {c: x if callable(x) else lambda rs: rs.chunks(x)
              for c, x in d.items()}

        def rec(rs, cs):
            if len(cs) != 0:
                c = cs[0]
                for i, rs1 in enumerate(d1[c](rs.isnum(c).order(c)), 1):
                    rs1[prefix + c] = i
                    rec(rs1, cs[1:])
        if dep:
            rec(self, list(d1))
        else:
            for c, fn in d1.items():
                for i, rs1 in enumerate(fn(self.isnum(c).order(c)), 1):
                    rs1[prefix + c] = i
        # return value not so important
        return self

    # Copy column values from rs
    def follow(self, rs, idcol, cols):
        cols = listify(cols)
        # initialize
        for c in list(cols):
            self[c] = ''
        # Now they must have the same columns
        rs1 = rs + self
        # Python sort perserves orders
        for rs2 in rs1.group(idcol):
            for c in list(cols):
                rs2[c] = rs2[0][c]
        # side effects method, return value not so important
        return self


class SQLPlus:
    def __init__(self, dbfile, cache_size, temp_store):
        """
        Args:
            dbfile (str): db filename or ':memory:'
        """
        global WORKSPACE

        # set workspace if it's not there
        if not WORKSPACE:
            if os.path.isabs(dbfile):
                WORKSPACE = os.path.dirname(dbfile)
            elif os.path.dirname(dbfile):
                WORKSPACE = os.path.join(os.getcwd(), os.path.dirname())
            else:
                # default workspace
                WORKSPACE = os.path.join(os.getcwd(), '')

        if not os.path.exists(WORKSPACE):
            os.makedirs(WORKSPACE)

        if dbfile != ':memory:':
            dbfile = os.path.join(WORKSPACE, os.path.basename(dbfile))

        # you may want to pass sqlite3.deltypes or something like that
        # but at this moment I think that will make matters worse
        self.conn = sqlite3.connect(dbfile)

        # row_factory is problematic don't use it
        # you can avoid the problems but not worth it
        # if you really need performance then just use "run"
        self._cursor = self.conn.cursor()
        # cursor for insertion only
        self._insert_cursor = self.conn.cursor()

        # some performance tuning
        self._cursor.execute(f'PRAGMA cache_size={cache_size}')
        self._cursor.execute('PRAGMA synchronous=OFF')
        self._cursor.execute('PRAGMA count_changes=0')
        # temp store at memory
        self._cursor.execute(f'PRAGMA temp_store={temp_store}')
        self._cursor.execute('PRAGMA journal_mode=OFF')

        # load some user-defined functions from util.py, istext unnecessary
        self.conn.create_function('isnum', -1, isnum)

    def fetch(self, tname, cols=None, where=None,
              order=None, group=None, roll=None):
        """Generates a sequence of rows from a table.
        """
        # At most one among order, group and roll
        if (1 if order else 0) + (1 if group else 0) + (1 if roll else 0) > 1:
            raise ValueError("""At most one arg allowed
                                among order, group and roll""")
        # set implicit order
        if group:
            order = group
        elif roll:
            size, step, dcol, *nextfn = roll
            order = dcol

        qrows = self._cursor.execute(_build_query(tname, cols, where, order))
        columns = [c[0] for c in qrows.description]
        # there can't be duplicates in column names
        if len(columns) != len(set(columns)):
            raise ValueError('duplicates in columns names')

        rows = _build_rows(qrows, columns)
        if group:
            for _, rs in groupby(rows, _build_keyfn(group)):
                yield Rows(rs)
        elif roll:
            nextfn = nextfn[0] if nextfn else None
            for ls in _roll(rows, size, step, _build_keyfn(dcol), nextfn):
                yield Rows(ls)
        else:
            yield from rows

    def insert(self, rs, name, overwrite=False, pkeys=None):
        # rs: Row, Rows, A seq of Row(s)
        if isinstance(rs, Row):
            r0 = rs
        elif isinstance(rs, Rows):
            if len(rs) == 0:
                return
            else:
                r0 = rs[0]
        else:
            try:
                r0, rs = peek_first(rs)
            except:
                # empty sequence
                return

        cols = r0.columns
        n = len(cols)

        name0 = name
        name1 = 'temp_' + random_string(20) if overwrite else name

        try:
            # create a table if not exists
            # You can't use self.tables because it uses the main cursor
            query = self._insert_cursor.execute("""
            select * from sqlite_master where type='table'
            """)
            if name1.lower() not in (row[1] for row in query):
                self._insert_cursor.execute(
                    _create_statement(name1, cols, pkeys))

            istmt = _insert_statement(name1, n)
            if isinstance(rs, Row):
                self._insert_cursor.execute(istmt, r0.values)
            else:
                self._insert_cursor.executemany(istmt, (r.values for r in rs))
        finally:
            if name0 != name1:
                self.rename(name1, name0)

    def write(self, filename, name=None, encoding='utf-8', pkeys=None):
        """
        """
        fn, ext = os.path.splitext(filename)

        if ext == '.csv':
            seq = _read_csv(filename, encoding)
        elif ext == '.xlsx':
            seq = _read_excel(filename)
        elif ext == '.sas7bdat':
            seq = _read_sas(filename)
        else:
            raise ValueError('Unknown file extension', ext)

        name = name or fn
        self.drop(name)
        self.insert(seq, name, True, pkeys)

    # register function to sql
    def register(self, fn, name=None):
        def newfn(*args):
            try:
                return fn(*args)
            except:
                return ''

        args = []
        for p in inspect.signature(fn).parameters.values():
            if p.kind != p.VAR_POSITIONAL:
                args.append(p)
        n = len(args) if args else -1
        name = name or fn.__name__
        self.conn.create_function(name, n, newfn)

    # register aggregate function to sql
    def register_agg(self, fn, name=None):
        d = {}

        def finalize(self):
            try:
                return fn(*(x for x in zip(*self.rows)))
            except:
                return ''
        d['finalize'] = finalize

        args = []
        for p in inspect.signature(fn).parameters.values():
            if p.kind != p.VAR_POSITIONAL:
                args.append(p)
        n = len(args) if args else -1

        clsname = 'Temp' + random_string()
        name = name or fn.__name__
        self.conn.create_aggregate(fn.__name__, n,
                                   type(clsname, (AggBuilder,), d))

    @property
    def tables(self):
        "list[str]: column names"
        query = self._cursor.execute("""
        select * from sqlite_master
        where type='table'
        """)
        # **.lower()
        tables = [row[1].lower() for row in query]
        return sorted(tables)

    # args can be a list, a tuple or a dictionary
    # It is unlikely that we need to worry about the security issues
    # but still there's no harm. So...
    def sql(self, query):
        """Simply executes sql statement and update tables attribute

        query: SQL query string
        args: args for SQL query
        """
        return self._cursor.execute(query)

    def rows(self, tname, cols=None, where=None, order=None):
        return Rows(self.fetch(tname, cols, where, order))

    def df(self, tname, cols=None, where=None, order=None):
        return self.rows(tname, cols, where, order).df(cols)

    def drop(self, tables):
        " drop table if exists "
        tables = listify(tables)
        for table in tables:
            # you can't use '?' for table name
            # '?' is for data insertion
            self.sql(f'drop table if exists {table}')

    def rename(self, old, new):
        if old.lower() in self.tables:
            self.sql(f'drop table if exists { new }')
            self.sql(f'alter table { old } rename to { new }')

    def _cols(self, query):
        return [c[0] for c in self.sql(query).description]

    def _pkeys(self, tname):
        "Primary keys in order"
        pks = [r for r in self.sql(f'pragma table_info({tname})') if r[5]]
        return [r[1] for r in sorted(pks, key=lambda r: r[5])]

    def newtable(self, query, name=None, pkeys=None):
        """Create new table from query(select statement)
        """
        temp_name = 'table_' + random_string()
        tname = _get_name_from_query(query)
        # keep pkeys from the original table if not exists
        pkeys = listify(pkeys) if pkeys else self._pkeys(tname)
        name = name or tname
        try:
            self.sql(_create_statement(temp_name, self._cols(query), pkeys))
            self.sql(f'insert into {temp_name} {query}')
            self.sql(f'drop table if exists { name }')
            self.sql(f"alter table { temp_name } rename to { name }")
        finally:
            self.sql(f'drop table if exists { temp_name }')

    def join(self, *tinfos, name=None, pkeys=None):
        "simplified version of left join"
        # if name is not given first table name#
        # tinfo: [tname, cols, cols to match]
        # ['sample', 'col1, col2 as colx', 'col3, col4']
        def get_newcols(cols):
            # extract new column names
            # if there's any renaming
            result = []
            for c in listify(cols.lower()):
                a, *b = [x.strip() for x in c.split('as')]
                result.append(b[0] if b else a)
            return result

        # No name specified, then the first table name is the output table name
        name = name or tinfos[0][0]
        # rewrite tinfos if there's missing matching columns
        mcols0 = tinfos[0][2]

        # validity check, what if mcols is a list of more than 1 element?
        for x in tinfos:
            assert len(x) == 2 or len(x) == 3, f"Invalid Arg: {x}"
        tinfos = [[tname, cols, mcols[0] if mcols else mcols0]
                  for tname, cols, *mcols in tinfos]

        # Validity checks
        all_newcols = []
        # number of matching columns for each given table
        mcols_sizes = []
        for _, cols, mcols in tinfos:
            all_newcols += get_newcols(cols)
            mcols_sizes.append(len(listify(mcols)))

        assert len(all_newcols) == len(set(all_newcols)), "Column duplicates"
        assert len(set(mcols_sizes)) == 1,\
            "Matching columns must have the same sizes"

        tcols = []
        # write new temporary tables for performance
        for tname, cols, mcols in tinfos:
            newcols = [tname + '.' + c for c in listify(cols)]
            tcols.append((tname, newcols, listify(mcols)))

        tname0, _, mcols0 = tcols[0]
        join_clauses = []
        for tname1, _, mcols1 in tcols[1:]:
            eqs = []
            for c0, c1 in zip(mcols0, mcols1):
                if c1:
                    eqs.append(f'{tname0}.{c0} = {tname1}.{c1}')
            join_clauses.append(f"""
            left join {tname1}
            on {' and '.join(eqs)}
            """)
        jcs = ' '.join(join_clauses)
        allcols = ', '.join(c for _, cols, _ in tcols for c in cols)
        query = f"select {allcols} from {tname0} {jcs}"
        self.newtable(query, name, pkeys)


def _safe_values(rows, cols):
    "assert all rows have cols"
    for r in rows:
        assert r.columns == cols, str(r)
        yield r.values


def _pick(cols, seq):
    " pick only cols for a seq, similar to sql select "
    cols = listify(cols)
    for r in seq:
        r1 = Row()
        for c in cols:
            r1[c] = r[c]
        yield r1


def _build_keyfn(key):
    " if key is a string return a key function "
    # if the key is already a function, just return it
    if hasattr(key, '__call__'):
        return key
    colnames = listify(key)
    if len(colnames) == 1:
        col = colnames[0]
        return lambda r: r[col]
    else:
        return lambda r: [r[colname] for colname in colnames]


def _create_statement(name, colnames, pkeys):
    """create table if not exists foo (...)

    Note:
        Every type is numeric.
        Table name and column names are all lower cased
    """
    pkeys = [f"primary key ({', '.join(listify(pkeys))})"] if pkeys else []
    # every col is numeric, this may not be so elegant but simple to handle.
    # If you want to change this, Think again
    schema = ', '.join([col.lower() + ' ' + 'numeric' for col in colnames] +
                       pkeys)
    return "create table if not exists %s (%s)" % (name.lower(), schema)


def _insert_statement(name, ncol):
    """insert into foo values (?, ?, ?, ...)
    Note:
        Column name is lower cased

    ncol : number of columns
    """
    qmarks = ', '.join(['?'] * ncol)
    return "insert into %s values (%s)" % (name.lower(), qmarks)


def _build_query(tname, cols=None, where=None, order=None):
    "Build select statement"
    cols = ', '.join(listify(cols)) if cols else '*'
    where = 'where ' + where if where else ''
    order = 'order by ' + ', '.join(listify(order)) if order else ''
    return f'select {cols} from {tname} {where} {order}'


# sequence row values to rows
def _build_rows(seq_values, cols):
    "build rows from an iterator of values"
    for vals in seq_values:
        r = Row()
        for col, val in zip(cols, vals):
            r[col] = val
        yield r


def _get_name_from_query(query):
    """'select * from foo where ...' => foo
    """
    pat = re.compile(r'\s+from\s+(\w+)\s*')
    try:
        return pat.search(query.lower()).group(1)
    except:
        return None


def _roll(seq, period, jump, keyfn, nextfn):
    """generates chunks of seq for rollover tasks.
    seq is assumed to be ordered
    """
    def chunk(seq):
        fst, seq1 = peek_first(seq)
        k0 = keyfn(fst)
        for k1, sq in groupby(seq1, keyfn):
            if k0 == k1:
                k0 = nextfn(k1)
                # you must realize them first
                yield list(sq)
            else:
                # some missings
                while k0 < k1:
                    k0 = nextfn(k0)
                    yield []
                k0 = nextfn(k1)
                # you must realize them first
                yield list(sq)

    def chunk_unsafe(seq):
        for _, sq, in groupby(seq, keyfn):
            yield list(sq)

    gss = tee(chunk(seq) if nextfn else chunk_unsafe(seq), period)
    for i, gs in enumerate(gss):
        # consume
        for i1 in range(i):
            next(gs)

    for xs in islice(zip_longest(*gss, fillvalue=None), 0, None, jump):
        # this might be a bit inefficient for some cases
        # but this is convenient, let's just go easy,
        # not making mistakes is much more important
        result = list(chain(*(x for x in xs if x)))
        if len(result) > 0:
            yield result


def _read_csv(filename, encoding='utf-8'):
    "Loads well-formed csv file, 1 header line and the rest is data "
    def is_empty_line(line):
        """Tests if a list of strings is empty for example ["", ""] or []
        """
        return [x for x in line if x.strip() != ""] == []

    with open(os.path.join(WORKSPACE, filename),
              encoding=encoding) as fin:
        first_line = fin.readline()[:-1]
        columns = listify(first_line)
        ncol = len(columns)

        # reader = csv.reader(fin)
        # NULL byte error handling
        reader = csv.reader(x.replace('\0', '') for x in fin)
        for line_no, line in enumerate(reader, 2):
            if len(line) != ncol:
                if is_empty_line(line):
                    continue
                raise ValueError(
                    """%s at line %s column count not matched %s != %s: %s
                    """ % (filename, line_no, ncol, len(line), line))
            row1 = Row()
            for col, val in zip(columns, line):
                row1[col] = val
            yield row1


def _read_sas(filename):
    filename = os.path.join(WORKSPACE, filename)
    with SAS7BDAT(filename) as f:
        reader = f.readlines()
        # lower case
        header = [x.lower() for x in next(reader)]
        for line in reader:
            r = Row()
            for k, v in zip(header, line):
                r[k] = v
            yield r


# this could be more complex but should it be?
def _read_excel(filename):
    def read_df(df):
        cols = df.columns
        for i, r in df.iterrows():
            r0 = Row()
            for c, v in zip(cols, (r[c] for c in cols)):
                r0[c] = str(v)
            yield r0

    filename = os.path.join(WORKSPACE, filename)
    # it's OK. Excel files are small
    df = pd.read_excel(filename)
    yield from read_df(df)


