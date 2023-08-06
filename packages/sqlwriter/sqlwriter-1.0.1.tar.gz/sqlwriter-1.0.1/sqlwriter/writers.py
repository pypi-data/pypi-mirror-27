# -*- coding: utf-8 -*-
import datetime as dt
import re

import pandas as pd
from dateutil import parser

from unidecode import unidecode
from utils import binary_search_for_error, chunks


class SQLWriter(object):
    '''Object that allows for the easy writing of data to Microsoft SQL Server

    Parameters
    ----------
    server : string
        Microsoft SQL Server configured in config.yaml
    database : string
        Target database on server
    table_name : string
        Target table in database
    cols : array-like
        Data columns to write to, should be contained in columns of target
        table. Length must match data row length.
    write_limit : int, default 200
        Determined by net_buffer_length and average row length.
        Not sure what this is in microsoft
    truncate : Boolean, default False
        Truncate the table before writing data
    logger : Python logging object, default None
        output information from mysql writer
    progress : boolean, default False
        optional argument for progress bar while writing to table
    '''

    def __init__(self, conn, database, table_name, cols, write_limit=200, truncate=False, logger=None, progress=False):
        self.conn = conn
        self.curs = self.conn.cursor()
        self.flavor = re.findall(r"<type '(\w+)", str(self.conn.__class__))[0]
        self.database = database
        self.table_name = table_name
        self.db_table = self._get_db_table()
        self.cols = cols
        self.write_limit = write_limit
        self.truncate = truncate
        self.logger = logger
        self.progress = progress
        self.drop_cols = []
        self.description = self._get_description()
        self.insert_part = 'INSERT INTO {} ('.format(self.db_table) + ','.join(cols) + ') VALUES '
        self.fields = self._make_fields()

    def _get_db_table(self):
        if self.flavor == 'psycopg2':
            return self.table_name
        elif self.flavor == 'pymssql':
            return '{}.dbo.{}'.format(self.database, self.table_name) # TODO: needs to be schema specific
        else:
            raise KeyError('{} not supported'.format(self.flavor))

    def _log(self, msg, level):
        """
        Handles optional logging
        """
        if self.logger is None:
            pass
        elif self.logger == 'console':
            print('{} -  {} - {} - {}'.format(dt.datetime.now(), self.table_name, level.upper(), msg))
        else:
            if level == 'info':
                self.logger.info(msg)
            if level == 'warn':
                self.logger.warn(msg)
            if level == 'debug':
                self.logger.debug(msg)
            if level == 'error':
                self.logger.error(msg)

    def _get_description(self):
        """
        Selects 1 record from selected database table, and takes description
        from cursor object

        Returns
        -------
        desc : list
            list of tuples that describe each selected column
        """
        sql = {
            'pymssql': 'select top 1 %s from %s',
            'psycopg2': 'select %s from %s'
        }
        self.curs.execute(sql[self.flavor] % (','.join(self.cols), self.db_table))
        desc = self.curs.description
        diff_cols = set([x.lower() for x in self.cols]).symmetric_difference(set([x[0].lower() for x in desc]))
        if len(diff_cols) > 0:
            # BUG: wont work, will error at line 64
            self._log('uncommon columns found in incoming data', 'warn')
            self._log(', '.join(diff_cols), 'warn')
        return desc

    def _make_fields_pymssql(self):
        import pymssql
        string, datetime, date, numeric, other = [], [], [], [], []
        for i in range(len(self.description)):
            test = self.description[i][1]
            if test == pymssql.STRING.value:
                string.append(i)
            elif test == pymssql.DATETIME.value:
                datetime.append(i)
            elif test == pymssql.DECIMAL.value or test == pymssql.NUMBER.value:
                numeric.append(i)
            else:
                other.append(i)
        return string, datetime, date, numeric, other

    def _make_fields_psycopg2(self):
        import psycopg2
        string, datetime, date, numeric, other = [], [], [], [], []
        for i in range(len(self.description)):
            test = self.description[i][1]
            if test in psycopg2.STRING.values:
                string.append(i)
            elif test in psycopg2.DATETIME.values:
                datetime.append(i)
            elif test in psycopg2.NUMBER.values:
                numeric.append(i)
            elif test in (1082,):
                date.append(i)
            else:
                other.append(i)
        return string, datetime, date, numeric, other

    def _make_fields(self):
        """
        Iterates through description and determines each fields data types
        so they can be properly formatted during writing

        Returns
        -------
        fields: dictionary of lists
            field types and corresponding indexes
        """
        keys = ('string', 'datetime', 'date', 'numeric', 'other')
        if self.flavor == 'pymssql':
            values = self._make_fields_pymssql()
        elif self.flavor == 'psycopg2':
            values = self._make_fields_psycopg2()
        return dict(zip(keys, values))

    def _mogrify(self, row):
        """String formats data based on fields to be able to multi-insert into
        MySQL

        Parameters
        ---------
        row : array-like
            An array of data to be written to the columns in the target table

        Returns
        -------
        string:
            row formatted as string tuple for easy mysql writing
        """
        if isinstance(row, tuple):
            row = list(row)  # needs to be mutable
        for idx in self.fields['string']:
            try:
                row[idx] = "'{}'".format(str(row[idx]).replace("'", "")) if row[idx] else 'NULL'
            except UnicodeEncodeError:
                row[idx] = "'{}'".format(unidecode(row[idx])) if row[idx] else 'NULL'
        for idx in self.fields['datetime']:
            try:
                row[idx] = row[idx].strftime("'%Y-%m-%d %H:%M:%S'") if row[idx] else 'NULL'
            except AttributeError:
                row[idx] = parser.parse(row[idx])
                row[idx] = row[idx].strftime("'%Y-%m-%d %H:%M:%S'")
            except:
                self._log('failed to format {}'.format(row[idx]), 'error')
                row[idx] = 'NULL'
        for idx in self.fields['date']:
            row[idx] = "'{}'".format(row[idx]) if row[idx] else 'NULL'
            # row[idx] = row[idx].strftime("'%Y-%m-%d'") if row[idx] else 'NULL'
        for idx in self.fields['numeric']:
            if row[idx] == '':
                row[idx] = 'NULL'
            else:
                row[idx] = str(row[idx])
        for idx in self.fields['other']:
            row[idx] = str(row[idx]) if row[idx] else 'NULL'
        return '(%s)' % ','.join(row)

    def _truncate(self):
        # NOTE: I'm pretty sure this syntax is universal
        if self.truncate:
            self._log('truncating table {}'.format(self.table_name), 'info')
            self.curs.execute('TRUNCATE TABLE {}'.format(self.db_table))
            self.conn.commit()

    def write(self, rows):
        """Truncates table, formats strings in data and multi-inserts into MySQL

        Parameters
        ----------
        rows: array-like
            An array of arrays of data to be written to the target table
        """
        if isinstance(rows, pd.DataFrame):
            rows = rows.values

        self._truncate()
        if len(rows) == 0:
            self._log('no data written to {}'.format(self.table_name), 'warn')
            return
        self._log('writing {0:,} rows to {1}'.format(len(rows), self.table_name), 'info')
        queries = list(chunks(rows, self.write_limit))  # NOTE:  innefficient, maybe keep as generator? or asynchronos process
        if self.progress:
            from tqdm import tqdm
        else:
            def tqdm(x): return x
        for query in tqdm(queries):
            query = [self._mogrify(x) for x in query]
            try:
                self.curs.execute(self.insert_part + ','.join(query))
                self.conn.commit()
            except Exception as e:
                column, value = binary_search_for_error(self.insert_part, query, self.server)
                print(column, value)
                raise Exception(e)

    def close(self):
        self.curs.close()
        self.conn.close()
