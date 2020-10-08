#!/usr/bin/env python

from typing import Tuple
from sqlite3 import Error
from PySimpleGUI import Window, WIN_CLOSED

from src import database as db
from src.layout import ID_INDEX, TASK_INDEX, STATUS_INDEX, DUE_INDEX, LABEL_INDEX, edit_layout
from src import constants as const

def update_label_filter(window):
    with db.connection() as conn:
        try:
            c = conn.cursor()
            c.execute('SELECT label FROM tasks')
            labels = c.fetchall()
            labels = [''] + [tup[0] for tup in labels]
            window['label-filter-combo'].Update(values=labels)
        except Exception as e:
            print(e)

def handle_event(window: Window, event: str, values: dict) -> str:
    table = window['task-table'].get()
    selected_taskids = ','.join((str(table[row][ID_INDEX]) for row in values['task-table']))
    commit = False
    with db.connection() as conn:
        try:
            c = conn.cursor()
            if event == 'add-button':
                new_task = values['task-inputtext']
                if new_task:
                    c.execute(f"""INSERT INTO tasks (task, priority, status, due, label)
                                  VALUES ('{new_task}', 'Medium', 'Incomplete', '', '')"""
                             )
                commit = True

            elif event == 'delete-button' and selected_taskids:
                c.execute(f"DELETE FROM tasks WHERE taskid IN ({selected_taskids})")
                commit = True

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
                    commit = True

                if to_incomplete:
                    task_ids = ','.join(to_incomplete)
                    c.execute(f"""UPDATE tasks SET status='Incomplete' WHERE taskid IN ({task_ids})""")
                    commit = True

            elif event == 'edit-button' and selected_taskids:
                # get current values for requested task
                c.execute(f"SELECT task, priority, status, due, label FROM tasks WHERE taskid = {selected_taskids[0]}")
                task, priority, status, due, label = c.fetchall()[0]

                # update edit window with current values
                font = const.get_font()
                edit_window = Window('Edit', edit_layout(), font=font, resizable=False)
                edit_window.Finalize()
                window.Disappear()
                edit_window['edit-task-inputtext'].update(value=task)
                edit_window['edit-priority-combo'].update(value=priority)
                edit_window['edit-status-combo'].update(value=status)
                edit_window['edit-due-inputtext'].update(value=due)
                edit_window['edit-label-inputtext'].update(value=label)

                try:
                    while True:
                        event, values = edit_window.read()
                        if event == WIN_CLOSED or event == 'edit-cancel-button':
                            break

                        elif event == 'edit-save-button':
                            task = edit_window['edit-task-inputtext'].get()
                            priority = edit_window['edit-priority-combo'].get()
                            status = edit_window['edit-status-combo'].get()
                            due_date = edit_window['edit-due-inputtext'].get()
                            label = edit_window['edit-label-inputtext'].get()

                            c.execute(f"""UPDATE tasks SET task='{task}',
                                                           priority='{priority}',
                                                           status='{status}',
                                                           due='{due_date}',
                                                           label='{label}'
                                                        WHERE taskid IN ({selected_taskids})""")

                            commit = True
                            break

                    edit_window.close()
                    window.Reappear()

                except Exception as e:
                    print(e)
                    edit_window.close()
                    window.Reappear()

            if commit:
                conn.commit()
                update_label_filter(window)

        except Error as e:
            err_str = str(e)

        else:
            err_str = ''

    return err_str
