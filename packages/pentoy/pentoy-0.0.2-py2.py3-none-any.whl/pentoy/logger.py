# -*- coding: utf-8 -*-

import logging
import sys
from pentoy import __app__


class PentoyLogger:
    def __init__(self, name=__app__, level=logging.INFO):
        self.logger = logging.getLogger(name)
        self.logger.propagate = False
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter('%(levelname)-7s - %(message)s ')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(level)
