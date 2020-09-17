#!/usr/bin/env python

from typing import Tuple
from sqlite3 import Error
from PySimpleGUI import Window

from src import database as db
from src.layout import ID_INDEX, TASK_INDEX, STATUS_INDEX, DUE_INDEX, LABEL_INDEX

def handle_event(window: Window, event: str, values: dict) -> str:
    err_str = ''
    table = window['task-table'].get()
    selected_taskids = ','.join((str(table[row][ID_INDEX]) for row in values['task-table']))
    with db.connection() as conn:
        c = conn.cursor()
        if event == 'add-button':
            new_task = values['task-inputtext']
            if new_task:
                c.execute(f"""
                    INSERT INTO tasks (task, status)
                    VALUES ('{new_task}', 'Incomplete')
                    """)

        elif event == 'delete-button' and selected_taskids:
            try:
                c.execute(f"DELETE FROM tasks WHERE taskid IN ({selected_taskids})")
            except Error as e:
                err_str += e

        elif event =='status-button' and selected_taskids:
            for row in values['task-table']:
                new_status = 'Complete' if table[row][STATUS_INDEX] == 'Incomplete' else 'Incomplete'
                task_id = table[row][ID_INDEX]
                c.execute(f"""UPDATE tasks SET status='{new_status}' WHERE taskid={task_id}""")

        elif event == 'edit-button' and selected_taskids:
            pass

        if not err_str:
            conn.commit()
    return err_str