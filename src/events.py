#!/usr/bin/env python

from typing import Tuple
from sqlite3 import Error
from PySimpleGUI import Window

from src import database as db
from src.layout import ID_INDEX, TASK_INDEX, STATUS_INDEX, DUE_INDEX, LABEL_INDEX

def handle_event(window: Window, event: str, values: dict) -> str:
    table = window['task-table'].get()
    selected_taskids = ','.join((str(table[row][ID_INDEX]) for row in values['task-table']))
    with db.connection() as conn:
        try:
            c = conn.cursor()
            if event == 'add-button':
                new_task = values['task-inputtext']
                if new_task:
                    c.execute(f"""
                        INSERT INTO tasks (task, status)
                        VALUES ('{new_task}', 'Incomplete')
                        """)

            elif event == 'delete-button' and selected_taskids:
                c.execute(f"DELETE FROM tasks WHERE taskid IN ({selected_taskids})")

            elif event =='status-button' and selected_taskids:
                to_complete = []
                to_incomplete = []
                for row in values['task-table']:
                    if table[row][STATUS_INDEX] == 'Incomplete':
                        to_complete.append(str(table[row][ID_INDEX]))
                    else:
                        to_incomplete.append(str(table[row][ID_INDEX]))

                if to_complete:
                    task_ids = ','.join(to_complete)
                    c.execute(f"""UPDATE tasks SET status='Complete' WHERE taskid IN ({task_ids})""")

                if to_incomplete:
                    task_ids = ','.join(to_incomplete)
                    c.execute(f"""UPDATE tasks SET status='Incomplete' WHERE taskid IN ({task_ids})""")

            elif event == 'edit-button' and selected_taskids:
                pass

            conn.commit()

        except Error as e:
            err_str = str(e)

        else:
            err_str = ''

    return err_str
