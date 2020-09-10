#!/usr/bin/env python

from pathlib import Path
import PySimpleGUI as sg
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

config_file = Path('../config/config.yml')
try:
    with open(config_file.resolve(), 'r') as yaml_file:
        config = yaml.load(yaml_file)
except:
    config = {'theme': 'Default', 'font-family': 'Verdana', 'font-size': 14}

font = (config['font-family'], config['font-size'])

_layout =   [
                [sg.InputText(default_text='Enter a task', key='input-text', size=(45,), font=font)],
                [sg.Button(button_text='Add', key='add-button', font=font),
                 sg.Button(button_text='Edit', key='edit-button', font=font),
                 sg.Button(button_text='Delete', key='delete-button', font=font),
                 sg.Button(button_text='Complete', key='complete-button', font=font),
                 sg.Button(button_text='Incomplete', key='incomplete-button', font=font)
                ],
                [sg.Table(headings=['Task', 'Label', 'Status'],
                          values=[['This is an example task', '', 'Incomplete']],
                          key='task-table',
                          justification='left',
                          font=font,
                          num_rows=20)
                ]
            ]

def layout():
    return _layout