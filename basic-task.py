#!/usr/bin/env python

from pathlib import Path
import sqlite3
import PySimpleGUI as sg

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

from src.layout import layout
from src.event_handler import handle_event

if __name__ == '__main__':

    config_file = Path('./config/config.yml')
    try:
        with open(config_file.resolve(), 'r') as yaml_file:
            config = yaml.load(yaml_file)
    except:
        config = {'theme': 'Default', 'font-family': 'Verdana', 'font-size': 14}

    sg.theme(config['theme'])

    window = sg.Window('Basic Task', layout())
    window.Finalize()

    while True:  # Event Loop
        event, values = window.read()

        if event == sg.WIN_CLOSED:
            break
        else:
            err = handle_event(window, event, values)
            if err:
                print(f'Failed to handle {event} event: {err}')

    window.close()