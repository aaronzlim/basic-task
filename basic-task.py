#!/usr/bin/env python

from typing import Union, Tuple
from pathlib import Path
import sqlite3
from sqlite3 import Error
import PySimpleGUI as sg

from src import constants as const
from src.layout import layout
from src.events import handle_event, update_label_filter
from src.utils import hex2rgb, rgb2hex, rgb2grayscale, complement_color
from src import database as db

def fix_element_background_color(elements, new_color: Union[str, Tuple[int]]):
    """Change the background color for all Text and Frame elements.

    Text color will be black or white depending on the grayscale value
    of the background color requested.

    Arguments:
        elements (PySimpleGUI Widget): Elements to correct background and text color (window.AllKeysDict.values())
        new_color (Union[str, Tuple[int]]): New background color as hex string #RRGGBB or tuple (r, g, b)

    """
    if isinstance(new_color, str): # assuming a hex string
        new_color = hex2rgb(new_color)
    text_color = 'black' if rgb2grayscale(*new_color) > 127 else 'white'
    new_color = rgb2hex(*new_color)

    for element in elements:
        if isinstance(element, sg.Text):
            element.Update(background_color=new_color, text_color=text_color)
        elif isinstance(element, sg.Frame):
            element.Widget.config(background=new_color)
            for row in element.Rows:
                for elem in row:
                    elem.ParentRowFrame.config(background=new_color)

def get_update_query(window):
    # update the table
    label_filter = window['label-filter-combo'].get()
    status_filter = window['status-filter-combo'].get()
    text_filter = window['text-filter-inputtext'].get()
    update_query = 'SELECT taskid, task, priority, status, due, label FROM tasks'

    if label_filter or status_filter or text_filter:
        update_query += ' WHERE'

    if label_filter:
        update_query += f" label='{label_filter}'"

    if status_filter:
        if label_filter:
            update_query += ' AND'
        update_query += f" status='{status_filter}'"

    if text_filter:
        if label_filter or status_filter:
            update_query += ' AND'
        update_query += f"task LIKE '%{text_filter}%'"

    return update_query

if __name__ == '__main__':

    config = const.read_config()
    font = const.get_font()

    sg.theme(config['theme']) # set the theme (see ./config/themes.txt)

    window = sg.Window( 'Basic Task', layout(), font=font, resizable=False)
    window.Finalize()

    ### Some minor aesthetic changes ###
    # Not all elements use the theme background color.
    # The next few lines of code fix that.

    # get the current background color for the window
    curr_background_color = sg.theme_element_background_color()
    if curr_background_color[0] != '#': # it's using the "magic color" 1234567890
        curr_background_color = '#ffffff' # White

    fix_element_background_color(window.AllKeysDict.values(), new_color=curr_background_color)

    # Make the delete button red for visibility/safety
    window['delete-button'].update(button_color=(window['delete-button'].ButtonColor[0], '#7a0000'))

    if not const.DATABASE_FILE_PATH.parent.exists():
        const.DATABASE_FILE_PATH.parent.mkdir()

    if not const.DATABASE_FILE_PATH.exists():
        db.init()

    with db.connection() as conn:
        c = conn.cursor()
        c.execute(get_update_query(window))
        window['task-table'].update(values=c.fetchall())

    ### The Main Event Loop ###
    try:
        while True:

            update_label_filter(window)

            event, values = window.read()

            if event == sg.WIN_CLOSED:
                break
            else:
                err = handle_event(window, event, values)
                if err:
                    sg.popup_error(f'Failed to handle {event} event: {err}', title='Error', font=font)

                with db.connection() as conn: # TODO: need to respond to enter button for text filter
                    c = conn.cursor()
                    c.execute(get_update_query(window))
                    window['task-table'].update(values=c.fetchall())

    except Exception as e:
        raise(e)

    finally:
        window.close()