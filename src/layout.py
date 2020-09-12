#!/usr/bin/env python

from pathlib import Path
import PySimpleGUI as sg
import yaml
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

config_file = Path('../config/config.yml')
try:
    with open(config_file.resolve(), 'r') as yaml_file:
        config = yaml.load(yaml_file, Loader=Loader)
except:
    config =    {
                    'theme': 'Default',
                    'font-family': 'Verdana',
                    'font-size': 14,
                }

_layout =   [
                [ # Task input text
                    sg.InputText(default_text='Enter a task', key='task-inputtext', size=(52,)),
                    sg.Button(button_text='Add', key='add-button'),
                ],
                [ # Filter bar
                    sg.Text('Label', key='label-text'),
                    sg.Combo(default_value='', values=[], key='label-filter-combo'),
                    sg.Button(button_text='Edit', key='edit-button'),
                ],
                [
                    sg.Text('Status', key='status-text'),
                    sg.Combo(key='status-filter-combo', default_value='All', values=['All', 'Complete', 'Incomplete'], readonly=True),
                    sg.Button(button_text='Status', key='status-button'),
                ],
                [
                    sg.Text('Contains Text', key='contains-text'),
                    sg.InputText(default_text='', key='text-filter-inputtext', size=(20,)),
                    sg.Button(button_text='Delete', key='delete-button')
                ],
                [ # Task table
                    sg.Table(   headings=['Task', 'Label', 'Status'],
                                values=[['', '', '']],
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