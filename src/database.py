#!/usr/bin/env python

from pathlib import Path
import sqlite3
from sqlite3 import Error
from contextlib import contextmanager

from src import constants

_INIT_SQL = \
"""
CREATE TABLE IF NOT EXISTS tasks(
    taskid INTEGER PRIMARY KEY AUTOINCREMENT,
    task TEXT NOT NULL UNIQUE,
    status TEXT DEFAULT 'Incomplete',
    due TEXT,
    label TEXT
)
"""
def init_sql():
    return _INIT_SQL

@contextmanager
def connection(db_path: str = constants.DATABASE_FILE_STR) -> sqlite3.Connection:
    """Context Manager for a connection to a sqlite database"""
    conn = None
    try:
        conn = sqlite3.connect(db_path)
        yield conn
    except Error as e:
        print(f'SQLITE ERROR: {e}')
    finally:
        if conn is not None:
            conn.close()

def init(db_path: str = constants.DATABASE_FILE_STR):
    """Generate a new database if none exists and create the correct tables."""
    with connection() as conn:
        conn.cursor().execute(init_sql())

