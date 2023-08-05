"""
A simple relational database interface that stays out of your way.
Designed to be small, fast, and transparent. Integrates with user-defined record classes.

* Record:     base class for user-defined Record classes (inherits from bl.dict.Dict)
* RecordSet:  set of Records (inherits from list)
* Database :  a database connection
                (init with a standard DB-API 2.0 connection string)

---------------------------------------------------------------------------
                                            Memory:  Footprint:
# > python                                  4656 K   4656 K (Python 3.4.3 OSX)
# >>> from bl.database import Database      5460 K    804 K (YMMV)
---------------------------------------------------------------------------
Sample session: 
>>> d = Database()      # in-memory sqlite3 database
>>> d.execute("create table table1 (name varchar primary key, email varchar not null unique)")
>>> d.execute("insert into table1 (name, email) values ('sah', 'sah@blackearthgroup.com')")
>>> records = d.select("select * from table1")
>>> records[0].name
'sah'
>>> d.connection.close()
>>>
"""

import datetime, imp, re, time, logging
from bl.dict import Dict

LOG = logging.getLogger(__name__)

class Database(Dict):
    """a database connection object."""

    def __init__(self, connection_string, adaptor=None, tries=3, minconn=1, maxconn=1, poolkey=None, **args):
        Dict.__init__(self, connection_string=re.sub('\s+', ' ', connection_string or ''), 
            adaptor=adaptor, tries=tries, minconn=minconn, maxconn=maxconn, **args)
        if self.adaptor is None: 
            if self.connection is not None:
                self.adaptor = self.connection.__module__
            else:
                import sqlite3
                self.adaptor = sqlite3
        if type(self.adaptor) in (str, bytes):
            self.adaptor = imp.load_module(self.adaptor, *imp.find_module(self.adaptor))
        
        if self.adaptor.__name__ == 'psycopg2':
            from psycopg2.pool import ThreadedConnectionPool
            self.pool = ThreadedConnectionPool(self.minconn or 1, self.maxconn or 1, self.connection_string)
        try:
            if self.adaptor == 'sqlite3' or 'sqlite3' in str(self.adaptor):
                self.execute("pragma foreign_keys = ON")
        except:
            pass

    def __repr__(self):
        return "Database(adaptor=%s, connection_string='%s')" % (self.adaptor, self.connection_string)

    @property
    def connection(self):
        if self.__connection is None:
            if self.pool is not None:
                conn = self.pool.getconn(key=self.poolkey or id(self))
            else:
                for i in range(self.tries):
                    try: 
                        conn = self.adaptor.connect(self.connection_string)
                        break
                    except: 
                        if i==list(range(self.tries))[-1]:       # last try failed
                            raise
                        else:                               # wait a bit
                            time.sleep(2*i)                 # doubling the time on each wait
            self.__connection = conn
            LOG.warn("db: %r key: %r pool: %r conn: %r" % (id(self), self.poolkey, id(self.pool), id(conn)))
        return self.__connection

    def migrate(self, migrations=None):
        from .migration import Migration
        Migration.migrate(self, migrations=migrations or self.migrations)

    def cursor(self):
        """get a cursor for fine-grained transaction control."""
        cursor = self.connection.cursor()
        return cursor

    def execute(self, sql, vals=None, cursor=None):
        """execute SQL transaction, commit it, and return nothing. 
        If a cursor is specified, work within that transaction.
        """
        LOG.debug("%r vals=%r" % (sql, vals))
        try:
            c = cursor or self.connection.cursor()
            c.execute(sql, vals or [])
            if cursor is None:
                self.commit()
        except:
            if cursor is not None:
                cursor.connection.rollback()
            raise

    def commit(self):
        """commit the changes on the current connection."""
        self.connection.commit()

    def rollback(self):
        """rollback the changes on the current connection, aborting the transaction."""
        self.connection.rollback()

    def select(self, sql, vals=None, Record=None, RecordSet=None, cursor=None):
        """select from db and return the full result set.
        Required Arguments:
            sql: the SQL query as a string
        Optional/Named Arguments
            vals: any bound variables
            Record: the class (itself) that the resulting records should be
        """
        if Record is None:
            from .record import Record
        if RecordSet is None:
            from .recordset import RecordSet

        records = RecordSet()                   # Populate a RecordSet (list) with the all resulting
        for record in self.selectgen(sql, vals=vals, Record=Record, cursor=cursor):
            records.append(record)
        return records

    def selectgen(self, sql, vals=None, Record=None, cursor=None):
        """select from db and yield a generator"""
        c = cursor or self.cursor()
        self.execute(sql, vals=vals, cursor=c)

        if Record is None:
            from .record import Record

        # get a list of attribute names from the cursor.description
        attr_list = list()
        for r in c.description:
            attr_list.append(r[0])

        result = c.fetchone()
        while result is not None:
            record = Record(self)               # whatever the record class is, include another instance
            for i in range(len(attr_list)):     # make each attribute dict-able by name
                record[attr_list[i]] = result[i]
            yield record
            result = c.fetchone()

        if cursor is None:
            c.close()   # closing the cursor without committing rolls back the transaction.

    def select_one(self, sql, vals=None, Record=None, cursor=None):
        """select one record from db
        Required Arguments:
            sql: the SQL query as a string
        Optional/Named Arguments:
            vals: any bound variables
            Record: the class (itself) that the resulting records should be
        """
        c = cursor or self.cursor()
        self.execute(sql, vals, cursor=c)

        if Record is None:
            from .record import Record

        # get a list of attribute names from the cursor.description
        attr_list = list()
        for r in c.description:
            attr_list.append(r[0])
        result = c.fetchone()
        if result is None:
            record = None
        else:
            record = Record(self)
            for i in range(len(attr_list)):
                record[attr_list[i]] = result[i]
        if cursor is None:
            c.close()
        return record

    def quote(self, attr):
        """returns the given attribute in a form that is insertable in the insert() and update() methods."""
        t = type(attr)
        if t == type(None): return 'NULL'
        elif t == datetime.datetime:    # datetime -- put it in quotes
            return "'%s'" % str(attr)
        elif t == str:
            return self._quote_str(attr)
        elif t in [dict, Dict]:
            return "$$%s$$" % attr
        else:                           # boolean or number -- no quoting needed
            return str(attr).lower()

    def _quote_str(self, attr):
        """quote the attr string in a manner fitting the Database server, if known."""
        sn = self.servername().lower()
        if 'sqlserver' in sn or 'sqlite' in sn or 'mysql' in sn:
            # quote for sqlserver and sqlite: double '' to escape
            attr = "'%s'" % re.sub("'", "''", attr)
        elif 'postgres' in sn:
            attr = "$$%s$$" % attr
        else:
            if type(attr) == str:
                attr = "'%s'" % attr
            else:
                attr = "'%s'" % str(attr, 'UTF-8')
        return attr

    def servername(self):
        """return a string that describes the database server being used"""
        if type(self.adaptor) in [str, bytes]:
            return self.adaptor
        elif 'psycopg' in str(self.adaptor):
            return 'postgresql'
        elif 'sqlite' in str(self.adaptor):
            return 'sqlite'
        elif self.dbconfig is not None and self.dbconfig.server is not None:
            return self.dbconfig.server
        elif 'adodbapi' in str(self.connection): 
            return 'sqlserver'
        elif 'port=5432' in str(self.connection): 
            return 'postgresql'
        elif 'port=3306' in str(self.connection): 
            return 'mysql'
        else: 
            return ''
        
    def table_names(self):
        sn = self.servername().lower()
        if 'sqlite' in sn:
            names = [r.name for r in self.select("select name from sqlite_master where type='table'")]
        elif 'mysql' in sn:
            names = [r.values()[0] for r in self.select("show tables")]
        else:
            names = [r.table_name for r in self.select("select table_name from information_schema.tables")]
        return names

    def table_exists(self, table_name):
        sn = self.servername().lower()
        if 'sqlite' in sn:
            return self.select_one(
                "select * from sqlite_master where name=? and type='table' limit 1", (table_name,))
        elif 'mysql' in sn:
            return self.select_one(
                "show tables like %s", (table_name,))
        else:   
            # postgresql and sqlserver both use the sql standard here.
            return self.select_one(
                "select * from information_schema.tables where table_name=%s limit 1", (table_name,))

def doctests():
    """
    >>> d = Database()
    >>> d.execute("create table table1 (name varchar primary key, email varchar not null unique);")
    >>> d.execute("insert into table1 (name, email) values ('sah', 'sah@blackearthgroup.com')")
    >>> d.execute("insert into table1 (name, email) values ('sah', 'sah.harrison@gmail.com')")
    Traceback (most recent call last):
      ...
    sqlite3.IntegrityError: UNIQUE constraint failed: table1.name
    """

if __name__ == "__main__":
    import doctest
    doctest.testmod()
