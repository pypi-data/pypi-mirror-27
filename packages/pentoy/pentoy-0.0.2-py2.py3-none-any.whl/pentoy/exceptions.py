# -*- coding: utf-8 -*-

from click import ClickException


class PentoyException(ClickException):
    """Base exceptions"""


class ParseException(PentoyException):
    """Markdown parser exceptions"""


class ConfigException(ClickException):
    """Configure exceptions"""
