import os
import re
import arrow
import sqlalchemy
import psycopg2
import logging
import pandas as pd
from sqlalchemy import create_engine

#logging.getLogger().setLevel(logging.DEBUG)

DATABASE_URL="postgresql+psycopg2://%s:%s@%s/%s" % (
    os.environ['PGUSER'],
    os.environ['PGPASSWORD'],
    os.environ['PGHOST'],
    os.environ['PGDATABASE'],
)

engine = create_engine(DATABASE_URL)

def Q(querystring):
    logging.info(querystring)
    return pd.read_sql_query(querystring, engine, index_col='id')

def TS(tablename, date_column=None, more_sql=None):
    if tablename == 'raw_device_data' and date_column == None:
        date_column = 'image_timestamp'
    elif date_column == None:
        date_column = 'created_at'

    if more_sql == None:
        more_sql = ''

    query = 'SELECT %s, 1 as num from %s %s' % (date_column, tablename, more_sql)
    logging.info(query)
    return pd.read_sql_query(query, engine, index_col=date_column)

def split_delta_unit(d):
    m = re.match('(\d+)\s*(\S+)', d)
    if not m:
        raise Exception('AGO and HENCE take delta strings like "6D" or "3 years"')
    delta, unit = m.groups()
    if len(unit) == 1:
        unit = {
            'd': 'days',
            'm': 'months',
            'y': 'years',
        }[unit.lower()]
    if unit[-1] != 's':
        unit += 's'
    return int(delta), unit

def arrow_delta(sign, delta, unit=None, fromdate=None):
    if fromdate == None:
        fromdate = arrow.now()

    if unit == None:
        delta, unit = split_delta_unit(delta)

    return fromdate.replace(**{unit:sign*delta})

def AGO(*args, **kwargs):
    return arrow_delta(-1, *args, **kwargs).format('YYYY-MM-DD')

def HENCE(*args, **kwargs):
    return arrow_delta(+1, *args, **kwargs).format('YYYY-MM-DD')
