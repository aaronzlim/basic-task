#!/usr/bin/env python

from typing import Tuple
from PySimpleGUI import Window

from src import database as db

def handle_event(window: Window, event: str, values: dict) -> str:
    err_str = ''
    if event == 'add-button':
        new_task = values['task-inputtext']
        if new_task:
            with db.connection() as conn:
                conn.cursor().execute(f"""
                INSERT INTO tasks (task, status)
                VALUES ('{new_task}', 'Incomplete')
                """)
                conn.commit()

    elif event == 'delete-button':
        pass

    return err_str