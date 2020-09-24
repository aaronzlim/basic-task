#!/usr/bin/env python

from pathlib import Path
import yaml
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

# Path to the configuration YAML file
CONFIG_FILE_PATH = Path('./config/config.yaml')

# Default configuration parameters
DEFAULT_CONFIG =    {
                        'theme': 'DefaultNoMoreNagging',
                        'font-family': 'Futura',
                        'font-size': 12,
                    }

DATABASE_FILE_PATH = Path('./database/tasks.db')
DATABASE_FILE_STR = DATABASE_FILE_PATH.resolve()

def read_config():
    try:
        with open(CONFIG_FILE_PATH.resolve(), 'r') as yaml_file:
            config = yaml.load(yaml_file, Loader=Loader)
    except Exception as e:
        print(e)
        sg.popup_error('Config Error: Unable to load config file. Using default configuration.')
        config = DEFAULT_CONFIG

    return config

def get_font():
    config = read_config()
    return (config.get('font-family', DEFAULT_CONFIG['font-family']),
            config.get('font-size', DEFAULT_CONFIG['font-size']))