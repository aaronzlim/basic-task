#!/usr/bin/env python

from pathlib import Path
import PySimpleGUI as sg
import yaml
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

from src.constants import CONFIG_FILE_PATH, DEFAULT_CONFIG

try:
    with open(CONFIG_FILE_PATH.resolve(), 'r') as yaml_file:
        config = yaml.load(yaml_file, Loader=Loader)
except:
    print(f'Failed to open config file at {CONFIG_FILE_PATH.resolve()}')
    config = DEFAULT_CONFIG

_buttons_layout =   [
                        [
                            sg.Button(button_text='Add', key='add-button', size=(5, 1), pad=(6, 6)),
                            sg.Button(button_text='Edit', key='edit-button', size=(5, 1), pad=(6, 6)),
                        ],
                        [
                            sg.Button(button_text='Status', key='status-button', size=(5, 1), pad=(6, 6)),
                            sg.Button(button_text='Delete', key='delete-button', size=(5, 1), pad=(6, 6)),
                        ],
                    ]

_filters_layout =   [
                        [
                            sg.Text('Label', key='label-text', size=(10,1)),
                            sg.Combo(default_value='All', values=['All'], key='label-filter-combo',
                                     size=(15, 1), readonly=True, enable_events=True),
                        ],
                        [
                            sg.Text('Status', key='status-text', size=(10, 1)),
                            sg.Combo(key='status-filter-combo', default_value='All',
                                     values=['All', 'Complete', 'Incomplete'], size=(15, 1),
                                     readonly=True, enable_events=True),

                        ],
                        [
                            sg.Text('Contains Text', key='contains-text'),
                            sg.InputText(default_text='', key='text-filter-inputtext',
                                         size=(15, 1), enable_events=True),
                        ],
                    ]

_layout =   [
                [ # Task input text
                    sg.InputText(default_text='Enter a task', key='task-inputtext', size=(48,)),
                ],
                [
                    sg.Frame(title='Filter Options', layout=_filters_layout, key='filter-options-frame'),
                    sg.Frame(title='Actions', layout=_buttons_layout, key='actions-frame'),
                ],
                [ # Task table
                    sg.Table(   headings=['ID', 'Task', 'Priority', 'Status', 'Due', 'Label'],
                                values=[['', '', '', '', '', '']],
                                key='task-table',
                                justification='left',
                                num_rows=10,
                                col_widths=[5, 20, 6, 7, 8, 8],
                                auto_size_columns=False,
                                vertical_scroll_only=False
                            ),
                ]
            ]

ID_INDEX = 0
TASK_INDEX = 1
PRIORITY_INDEX = 2
STATUS_INDEX = 3
DUE_INDEX = 4
LABEL_INDEX = 5

def layout():
    return _layout

def filters_layout():
    return _filters_layout

def buttons_layout():
    return _buttons_layout

def edit_layout():
    # Layout must be generated with each call.
    # PySimpleGUI does not allow object reuse.
    return  [
                [
                    sg.Text('Task', key='edit-task-text', pad=((3, 17), (3, 3))),
                    sg.InputText(key='edit-task-inputtext', size=(20, 1))
                ],
                [
                    sg.Text('Priority', key='edit-priority-text', pad=((3, 0), (3, 3))),
                    sg.Combo(values=['Low', 'Medium', 'High', 'Top'], default_value='Medium',
                             key='edit-priority-combo')
                ],
                [
                    sg.Text('Status', key='edit-status-text', pad=((3, 7), (3, 3))),
                    sg.Combo(values=['Complete', 'Incomplete'], default_value='Incomplete', key='edit-status-combo')
                ],
                [
                    sg.Text('Due (MM/DD/YYYY)', key='edit-due-text', pad=((3, 0), (3, 3))),
                    sg.InputText(key='edit-due-inputtext', size=(10, 1)),
                    sg.CalendarButton('Date',
                                      key='edit-due-calendarbutton',
                                      size=(6, 1),
                                      close_when_date_chosen=True,
                                      format='%m/%d/%Y',
                                      target='due-inputtext',
                                     )
                ],
                [
                    sg.Text('Label', key='edit-label=text', pad=((3, 13), (3, 3))),
                    sg.InputText(key='edit-label-inputtext', size=(20, 1))
                ],
                [
                    sg.Button('Save', key='edit-save-button', size=(6, 1), pad=((3, 20), (3, 3))),
                    sg.Button('Cancel', key='edit-cancel-button', size=(6, 1))
                ]
            ]