# -*- coding: utf-8 -*-
import os
import threading
import logging
from collections import deque
from jinja2 import (Environment, Template, BaseLoader, ChoiceLoader,
                    PrefixLoader, FileSystemLoader, TemplateNotFound)

from pentoy.parser import MarkdownParser

logger = logging.getLogger(__name__)


class PentoyTemplateNotFound(Exception):
    pass


# env = Environment(loader=FileSystemLoader('boilerplate/scaffolds'))
# template = env.get_template('post.md')
# output_from_parsed_template = template.render(title='Test', date='2017-12-04')
# print(output_from_parsed_template)


class Builder:
    """Build static site files."""

    def __init__(self, ctx, theme, src_path, dst_path, **kwargs):
        self.cxt = ctx
        self.theme = theme
        self.src_path = src_path
        self.dst_path = dst_path

        for k, v in kwargs.items():
            setattr(self, k, v)

        try:
            os.makedirs(dst_path)
        except OSError:
            pass

    def build(self, src):
        pass

    def read_tree(self):
        pass

    def full_build(self):
        """Build all source files."""
        queue = self.dst_path

    def incremental_build(self):
        """Build changed files only."""
        pass


class BackgroundBuilder(threading.Thread):
    """Execute building on background."""

    def __init__(self, src_path, dst_path):
        threading.Thread.__init__(self)
        self.src_path = src_path
        self.dst_path = dst_path

    def run(self):
        # TODO: build source on-the-fly.
        self.build()

    def build(self):
        builder = Builder(self.src_path, self.dst_path)
        builder.full_build()
