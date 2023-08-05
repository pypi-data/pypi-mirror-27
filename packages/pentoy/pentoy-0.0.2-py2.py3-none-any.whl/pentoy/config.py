# -*- coding: utf-8 -*-

import logging
import os
import yaml

from pentoy.logger import *

logger = logging.getLogger(__name__)

DEFAULT_CONFIG = {
    'theme': '',
}


def load_config_file(path, default_config=DEFAULT_CONFIG):
    """Load user config from pentoy.yml"""
    name, ext = os.path.splitext(os.path.basename(path))
    if ext not in ['yml', 'yaml']:
        raise FileNotFoundError

    config = None
    with open(path, 'r') as f:
        try:
            config = yaml.load(f)
        except yaml.YAMLError as e:
            logger.error(str(e))
    return config


def load_config(path=None, file=''):
    pass
