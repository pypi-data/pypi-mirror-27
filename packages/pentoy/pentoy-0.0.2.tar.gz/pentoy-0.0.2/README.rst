Pentoy is a light note generator powered by Python_.
====================================================

.. image:: https://img.shields.io/pypi/v/pentoy.svg
    :target: https://pypi.python.org/pypi/pentoy

.. image:: https://img.shields.io/pypi/l/pipenv.svg
    :target: https://pypi.python.org/pypi/pipenv

------------------------

What does "Pentoy" mean?
------------------------
**Pentoy** is combined with "Py" and "Note", obviously means what does it do and what makes it. It's also a pen and a toy.

.. Links

.. _Python: http://www.python.org

Installation
------------

::

  $ pip install pentoy



Commands
------------

1. Create a Pentoy site::

    mkdir pentoy-demo
    pentoy init

2. Create a new post::

    pentoy new 'first_note'

3. Build files::

    pentoy build

4. Preview your site::

    pentoy serve

Usage
-----

::

    $ pentoy
    Usage: pentoy [OPTIONS] COMMAND [ARGS]...

      Pentoy - A light note generator powered by Python.

    Options:
      -h, --help       Show this message and exit
      --update         Update to latest.
      -j, --jumbotron  Fun.
      --version        Show the version and exit.


    Usage Examples:
       Create a new site:
       $ pentoy init

       Post a new article:
       $ pentoy new

       Serve your site:
       $ pentoy server

       Deploy your site:
       $ pentoy deploy

       Clear your generated files:
       $ pentoy clean

    Commands:
      build   Build your articles.
      clear   Clean your generated files.
      deploy  Deploy your site.
      init    Create an empty pentoy static site.
      new     Create a new article.
      server  Serve your site.
      test    Test for cli

LICENSE
-------

MIT License

Copyright (c) 2017 sudoz

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.