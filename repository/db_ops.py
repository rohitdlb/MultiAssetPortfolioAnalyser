import logging
import os
import sqlite3

import pandas as pd

from utils.constants import MY_DATABASE, FACTOR_DEFINITION_TABLE, EQUITY_INDEX_TABLE, MACRO_INDEX_TABLE

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())


db_file = 'file:{}/repository/{}.sqlite3'.format(os.getcwd(), MY_DATABASE)
conn = sqlite3.connect(db_file, check_same_thread=False, uri=True)


def write_data_to_db(data, table_name):
    data.to_sql(table_name, con=conn, index=False, if_exists='append')


def check_if_tables_already_exist():
    cursor = conn.cursor()
    list_of_tables = cursor.execute(
        """SELECT tbl_name FROM sqlite_master WHERE type='table' """).fetchall()
    if len(list_of_tables) == 0:
        return False
    return True


def create_equity_indices_table():
    cursor = conn.cursor()
    # Create table for storing equity indices data
    cursor.execute('''CREATE TABLE IF NOT EXISTS {}
                     (ticker TEXT,
                      date INTEGER,
                      level REAL,
                      delta REAL,
                      PRIMARY KEY (ticker, date))'''.format(EQUITY_INDEX_TABLE))
    conn.commit()
    logger.info('Equity Indices Table created successfully')


def create_factor_definition_table():
    cursor = conn.cursor()
    # Create table for storing equity indices data
    cursor.execute('''CREATE TABLE IF NOT EXISTS {}
                         (macro_factor_tag TEXT PRIMARY KEY,
                          type TEXT)'''.format(FACTOR_DEFINITION_TABLE))
    conn.commit()
    logger.info('Factor Definition Table created successfully')


def create_macro_indices_table():
    cursor = conn.cursor()
    # Create table for storing macros factor data
    cursor.execute('''CREATE TABLE IF NOT EXISTS {}
                     (macro_factor_tag TEXT,
                      date INTEGER,
                      level REAL,
                      delta REAL,
                      PRIMARY KEY (macro_factor_tag, date))'''.format(MACRO_INDEX_TABLE))
    conn.commit()
    logger.info('Macro (Level/Delta) Indices Table created successfully')


def get_equity_indices_data(list_indices, start_date, end_date):
    query = '''SELECT ticker AS factor, date, delta AS data FROM {} WHERE ticker IN {} AND DATE BETWEEN {} AND {} 
        ORDER BY ticker, date'''.format(EQUITY_INDEX_TABLE, tuple(list_indices), start_date, end_date)
    logger.info(f"Executing query: \n {query}")
    df_out = pd.read_sql_query(query, conn)
    return df_out


def get_equity_indices_level_data(list_indices, start_date, end_date):
    query = '''SELECT ticker AS factor, date, level AS data FROM {} WHERE ticker IN {} AND DATE BETWEEN {} AND {} 
        ORDER BY ticker, date'''.format(EQUITY_INDEX_TABLE, tuple(list_indices), start_date, end_date)
    logger.info(f"Executing query: \n {query}")
    df_out = pd.read_sql_query(query, conn)
    return df_out


def get_macro_factors_data(list_factors, start_date, end_date):
    query = '''SELECT a.macro_factor_tag AS factor, a.date,
       CASE WHEN b.type = 'delta' THEN delta ELSE level END data
    FROM macro_indices a LEFT JOIN factor_definition b ON a.macro_factor_tag = b.macro_factor_tag
    WHERE a.date between {} and {} AND a.macro_factor_tag IN {}'''.format(start_date, end_date, tuple(list_factors))
    logger.info(f"Executing query: \n {query}")
    df_out = pd.read_sql_query(query, conn)
    return df_out
