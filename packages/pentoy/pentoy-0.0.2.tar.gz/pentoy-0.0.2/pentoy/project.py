# -*- coding: utf-8 -*-
import os

from . import __app__
from pentoy.utils import get_temp_dir
from pentoy.constants import CFG_FILENAME, CFG_MARK, POST_DIR, DRAFT_DIR, \
    SCAFFOLD_DIR
from jinja2 import Environment, FileSystemLoader


class Pentoy(object):
    """Docstring for Pentoy
    `pentoy.yml` is the only evidence indicate it is a pentoy project,
    and this directory is the root path of pentoy project.
    """

    def __init__(self):
        super(Pentoy, self).__init__()
        self._name = None
        self._cfg_path = None
        self._original_dir = os.path.abspath(os.curdir)

        try:
            os.chdir(self.project_path)
        except (TypeError, AttributeError):
            pass

    @property
    def name(self):
        if self._name is None:
            self._name = self.config_path.split(os.sep)[-2]
        return self._name

    @property
    def is_under_project(self):
        """Check pwd is under a pentoy project."""
        while os.getcwd() is not '/':
            if os.path.exists(os.path.join(os.getcwd(), CFG_FILENAME)):
                with open(os.path.join(os.getcwd(), CFG_FILENAME), 'r') as f:
                    if f.readline().strip() == CFG_MARK:
                        return True
                    else:
                        os.chdir(os.pardir)
            else:
                os.chdir(os.pardir)
        return False

    @property
    def config_exists(self):
        return bool(self._cfg_path)

    @property
    def project_path(self):
        if self.config_exists:
            return os.path.abspath(os.path.join(self.config_path, os.pardir))
        return None

    @property
    def post_path(self):
        if self.config_exists:
            return os.path.abspath(os.path.join(self.project_path, POST_DIR))
        return None

    @property
    def draft_path(self):
        if self.config_exists:
            return os.path.abspath(os.path.join(self.project_path, DRAFT_DIR))
        return None

    @property
    def config_path(self):
        if self._cfg_path is None:
            try:
                path = os.path.join(os.getcwd(), CFG_FILENAME)
            except RuntimeError:
                path = None
            self._cfg_path = path

        return self._cfg_path

    @property
    def project_exists(self):
        return bool(self.config_path)
        # return bool(self.project_path)

    @property
    def project_emtpy(self):
        return os.listdir(self.project_path) == []

    @property
    def template_env(self):
        env = Environment(loader=FileSystemLoader(os.path.join(self.project_path, SCAFFOLD_DIR)))
        tpl = env.get_template('post.md')
        return tpl

    def get_default_path(self):
        return os.path.join(self.project_path, 'public')

    def get_temp_path(self):
        return os.path.join(get_temp_dir(__app__), 'public')

    def to_json(self):
        return {
            '_name': self._name,
            '_config_path': self._cfg_path,
            '_original_dir': self._original_dir,
            'project_path': self.project_path,
            'config_path': self.config_path,
            'public_path': self.get_default_path(),
            'post_path': self.post_path,
            'draft_path': self.draft_path
        }
