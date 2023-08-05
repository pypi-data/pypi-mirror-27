# -*- coding: utf-8 -*-
import os
import datetime
import re
import sys
import shutil
import tempfile


def get_py_ver():
    return sys.version_info


def get_cur_date():
    return datetime.datetime.today().strftime('%Y-%m-%d')


def get_now_datetime():
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def format_title(title):
    return '-'.join((''.join(re.split(r'[()]', title)).split()))


def get_abs_dir(name):
    return os.path.abspath(os.path.join(name, os.pardir))


def get_temp_dir(name):
    return os.path.join(tempfile.gettempdir(), name)


def copytree(src, dst, symlinks=False, ignore=None):
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, symlinks, ignore)
        else:
            shutil.copy2(s, d)


def rmtree(path, ignore=False):
    if os.path.exists(path):
        shutil.rmtree(path, ignore)


def mkdir_p(path):
    """work as command `mkdir -p`"""
    if os.path.isdir(path):
        pass
    elif os.path.isfile(path):
        raise OSError("the path name is as same as an existing file's name")
    else:
        (upper_dir, lower_dir) = os.path.split(path)
        if upper_dir and not os.path.isdir(upper_dir):
            mkdir_p(upper_dir)
        if lower_dir:
            os.mkdir(path)


def test():
    return os.path.dirname(os.path.abspath(__file__))


if __name__ == '__main__':
    print(get_temp_dir('pentoy'))
