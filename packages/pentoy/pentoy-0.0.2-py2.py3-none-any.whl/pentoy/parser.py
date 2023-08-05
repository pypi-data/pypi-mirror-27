# -*- coding: utf-8 -*-
import logging
import mistune
import threading

from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import html
from pygments.util import ClassNotFound

logger = logging.getLogger(__name__)

DB_JSON = {
    'category': '',
    'tag': ''
}


class BaseParser:
    """Base parser."""

    def __init__(self, config):
        self.config = config

    def gen_metadata(self):
        pass

    def parse(self, src_path):
        result = None
        return result


class MarkdownParser(BaseParser):
    """Parser for markdown files."""
    supported_ext = ['md', 'markdown', 'mdown', 'mkdn', 'mkd']

    def __init__(self, *args, **kwargs):
        super(MarkdownParser, self).__init__(*args, **kwargs)
        self._src_path = None

    def parse(self, src_path):
        """Pull the trigger."""
        self._src_path = src_path


class CodeRender(mistune.Renderer):
    """Code syntax highlight render."""

    def __init__(self, **kwargs):
        super(CodeRender, self).__init__(**kwargs)

    def block_code(self, code, lang=None):
        if not lang:
            return '\n<pre><code>%s</code></pre>\n' % mistune.escape(code)
        try:
            lexer = get_lexer_by_name(lang, stripall=True)
            formatter = html.HtmlFormatter()
            return highlight(code, lexer, formatter)
        except ClassNotFound:
            return super(CodeRender, self).block_code(code, lang)


class HeadRender(mistune.Renderer):
    pass


class ImageRender(mistune.Renderer):
    """Special render for images"""
    pass


def parse_markdown():
    """Parse *.md to *.html files"""
    pass


def create_markdown():
    """Create customized markdown,
    it is better to reuse the Markdown instance.
    """
    render = CodeRender()
    return mistune.Markdown(renderer=render)
