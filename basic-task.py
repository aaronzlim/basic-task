#!/usr/bin/env python

from typing import Union, Tuple
from pathlib import Path
import sqlite3
from sqlite3 import Error
import PySimpleGUI as sg

import yaml
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

from src.constants import CONFIG_FILE_PATH, DEFAULT_CONFIG, DATABASE_FILE_PATH
from src.layout import layout
from src.events import handle_event
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

if __name__ == '__main__':

    ### Load the config file ###
    try:
        with open(CONFIG_FILE_PATH.resolve(), 'r') as yaml_file:
            config = yaml.load(yaml_file, Loader=Loader)
    except Exception as e:
        print(e)
        print('Using default configuration.')
        config = DEFAULT_CONFIG

    sg.theme(config['theme']) # set the theme (see ./config/themes.txt)

    window = sg.Window('Basic Task', layout(),
                       font=(config.get('font-family', DEFAULT_CONFIG['font-family']),
                             config.get('font-size', DEFAULT_CONFIG['font-size'])
                            )
                      )
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
    window['delete-button'].update(button_color=(window['delete-button'].ButtonColor[0], 'red'))

    if not DATABASE_FILE_PATH.exists():
        db.init()

    ### The Main Event Loop ###
    while True:
        event, values = window.read()
        print(event, values)
        if event == sg.WIN_CLOSED:
            break
        else:
            err = handle_event(window, event, values)
            if err:
                print(f'Failed to handle {event} event: {err}')

    window.close()