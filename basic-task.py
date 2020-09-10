#!/usr/bin/env python

import sqlite3
import PySimpleGUI as sg
from src.layout import layout
from src.event_handler import handle_event

if __name__ == '__main__':

    sg.theme('Default')

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