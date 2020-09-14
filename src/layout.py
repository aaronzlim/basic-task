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
                    sg.Table(   headings=['Task', 'Status', 'Due', 'Label'],
                                values=[['', '', '', '']],
                                key='task-table',
                                justification='left',
                                num_rows=20,
                                col_widths=[25, 10, 10],
                                auto_size_columns=False
                            ),
                ]
            ]

def layout():
    return _layout

def filters_layout():
    return _filters_layout

def buttons_layout():
    return _buttons_layout