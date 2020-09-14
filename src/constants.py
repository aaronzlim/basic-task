#!/usr/bin/env python

from pathlib import Path

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
