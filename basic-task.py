#!/usr/bin/env python

from typing import Union, Tuple
from pathlib import Path
import sqlite3
import PySimpleGUI as sg

import yaml
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

from src.layout import layout
from src.event_handler import handle_event
from src.utils import hex2rgb, rgb2hex, rgb2grayscale, complement_color

default_config = {'theme': 'DefaultNoMoreNagging',
                  'font-family': 'Futura',
                  'font-size': 12,
                 }

def fix_text_background_color(window, new_color: Union[str, Tuple[int]]):
    """Change the background color for all Text elements.
       Text color will be black or white depending on the grayscale value
       of the background color requested.
    """
    if isinstance(new_color, str): # assuming a hex string
        new_color = hex2rgb(new_color)
    text_color = 'black' if rgb2grayscale(*new_color) > 127 else 'white'
    new_color = rgb2hex(*new_color)

    for element in window.AllKeysDict.values():
        if isinstance(element, sg.Text):
            element.Update(background_color=new_color, text_color=text_color)

if __name__ == '__main__':

    config_file = Path('./config/config.yml')
    try:
        with open(config_file.resolve(), 'r') as yaml_file:
            config = yaml.load(yaml_file, Loader=Loader)
    except Exception as e:
        print(e)
        print('Using default configuration.')
        config = default_config

    sg.theme(config['theme'])

    window = sg.Window('Basic Task', layout(),
                       font=(config.get('font-family', default_config['font-family']),
                             config.get('font-size', default_config['font-size'])
                            )
                      )
    window.Finalize()
    curr_background_color = sg.theme_element_background_color()
    if curr_background_color[0] != '#':
        curr_background_color = '#ffffff'
    fix_text_background_color(window, new_color=curr_background_color)

    while True:  # Event Loop
        event, values = window.read()

        if event == sg.WIN_CLOSED:
            break
        else:
            err = handle_event(window, event, values)
            if err:
                print(f'Failed to handle {event} event: {err}')

    window.close()