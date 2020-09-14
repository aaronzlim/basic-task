#!/usr/bin/env python

from pathlib import Path
import sqlite3
from sqlite3 import Error

from src import constants

_INIT_SQL = \
"""
CREATE TABLE IF NOT EXISTS tasks(
    Task TEXT NOT NULL,
    Status TEXT DEFAULT 'Incomplete',
    Due TEXT,
    Label TEXT
)
"""
def init_sql():
    return _INIT_SQL

def connect(db_path: str = constants.DATABASE_FILE_STR) -> sqlite3.Connection:
    """Create a connection to a sqlite database"""
    conn = None
    try:
        conn = sqlite3.connect(db_path)
    except Error as e:
        print(e)
    finally:
        return conn

def init(db_path: str = constants.DATABASE_FILE_STR):
    """Generate a new database if none exists and create the correct tables."""
    if not Path(db_path).exists():
        try:
            conn = connect(db_path)
            c = conn.cursor()
            c.execute(init_sql())
        except Error as e:
            print(e)
        finally:
            conn.close()
