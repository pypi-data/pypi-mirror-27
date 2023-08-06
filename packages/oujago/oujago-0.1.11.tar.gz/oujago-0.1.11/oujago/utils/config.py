# -*- coding: utf-8 -*-

import json
import os
import sys


def set_config(configuration):
    """Configuration setting.

    Parameters
    ----------
    configuration : dict
        Global configuration.
    """
    with open(_config_path, 'w') as f:
        f.write(json.dumps(configuration, indent=4))


# global data path
DATA_PATH = None

if 'OUJAGO' not in os.environ:
    sys.stderr.write("WARNING: please add 'OUJAGO' variable to your PATH environment. "
                     "'export OUJAGO=<OUJAGO DATA PATH>'."
                     "\n"
                     "Or, use 'oujago.utils.set_data_path(<DATA_PATH>)' to set global model path.")
else:
    DATA_PATH = os.environ.get('OUJAGO')


# base oujago directory
_oujago_base_dir = os.path.expanduser('~')
if not os.access(_oujago_base_dir, os.W_OK):
    _oujago_base_dir = '/tmp'

_oujago_dir = os.path.join(_oujago_base_dir, '.oujago')
if not os.path.exists(_oujago_dir):
    os.makedirs(_oujago_dir)

# oujago configuration directory
_config_path = os.path.expanduser(os.path.join(_oujago_dir, 'oujago.json'))
if os.path.exists(_config_path):
    _config = json.load(open(_config_path))
else:
    _config = {
        'data_path': None
    }
    set_config(_config)


def get_config():
    """
    Publicly accessible method for configuration.

    Returns
    -------
    dict
        Global configuration.
    """
    return _config


def set_data_path(data_path):
    """Global `DATA_PATH` setting.

    Parameters
    ----------
    data_path : str
        Oujago needed model path.
    """
    global DATA_PATH
    if os.path.exists(data_path):
        DATA_PATH = data_path
    else:
        sys.stderr.write("WARNING: not a valid path, '{}' does not exist.".format(data_path))


def get_data_path():
    """Publicly accessible method for `DATA_PATH`.

    Returns
    -------
    str
        Global `DATA_PATH`.
    """

