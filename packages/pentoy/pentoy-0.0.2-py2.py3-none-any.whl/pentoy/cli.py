# -*- coding: utf-8 -*-
import sys
import os
import time
import logging
import click
import crayons
import background
import pkg_resources
import requests
import semver
from pentoy.constants import POST_SUFFIX, ConsoleLevel

from .utils import (get_cur_date, get_py_ver, format_title, copytree, rmtree)
from .project import Pentoy
from . import __app__
from .__version__ import __version__

# __________               __
# \______   \ ____   _____/  |_  ____ ___.__.
#  |     ___// __ \ /    \   __\/  _ <   |  |
#  |    |   \  ___/|   |  \  | (  <_> )___  |
#  |____|    \___  >___|  /__|  \____// ____|
#                \/     \/            \/

logger = logging.getLogger(__name__)

pentoy = Pentoy()

click.disable_unicode_literals_warning = True

IGNORED_PACKAGES = (
    'setuptools', 'pip', 'wheel', 'six', 'packaging', 'pyparsing', 'appdirs')

xyzzy = """
 _______                        __                          __ 
/       \                      /  |                        /  |
$$$$$$$  | ______   _______   _$$ |_     ______   __    __ $$ |
$$ |__$$ |/      \ /       \ / $$   |   /      \ /  |  /  |$$ |
$$    $$//$$$$$$  |$$$$$$$  |$$$$$$/   /$$$$$$  |$$ |  $$ |$$ |
$$$$$$$/ $$    $$ |$$ |  $$ |  $$ | __ $$ |  $$ |$$ |  $$ |$$/ 
$$ |     $$$$$$$$/ $$ |  $$ |  $$ |/  |$$ \__$$ |$$ \__$$ | __ 
$$ |     $$       |$$ |  $$ |  $$  $$/ $$    $$/ $$    $$ |/  |
$$/       $$$$$$$/ $$/   $$/    $$$$/   $$$$$$/   $$$$$$$ |$$/ 
                                                 /  \__$$ |    
                                                 $$    $$/     
"""


# TODO: crayons -> click.style
def puts(data, level=ConsoleLevel.INFO):
    """Replace click.echo()"""

    def puts_info():
        click.echo('{0}: {1}'.format(crayons.green('INFO'), data))

    def puts_warn():
        click.echo('{0}: {1}'.format(crayons.yellow('WARN'), data))

    def puts_error():
        click.echo('{0}: {1}'.format(crayons.red('ERROR'), data), err=True)

    return {
        ConsoleLevel.INFO: puts_info,
        ConsoleLevel.WARN: puts_warn,
        ConsoleLevel.ERROR: puts_error
    }.get(level)()


# Console prompt
USAGE_HELP = """
Usage Examples:
   Create a new site:
   $ {0}

   Post a new article:
   $ {1}

   Serve your site:
   $ {2}
   
   Deploy your site:
   $ {3}
   
   Clear your generated files:
   $ {4}

Commands:"""


# @background.task
def check_for_updates():
    """Background task"""
    try:
        r = requests.get('https://pypi.python.org/pypi/pentoy/json', timeout=1)
        latest = sorted([semver.parse_version_info(v) for v in
                         list(r.json()['releases'].keys())])[-1]
        current = semver.parse_version_info(__version__)

        if latest > current:
            puts(
                '{0}: {1} is now available. Run command ($ {})!'.format(
                    crayons.green('Courtesy Notice'),
                    crayons.yellow(
                        'Pentoy {v.major}.{v.minor}.{v.patch}'.format(
                            v=latest)),
                    crayons.red('pentoy --update')
                ), level='info')
    except Exception:
        pass


def echo_help(helper):
    """Formats the help"""
    helper = helper.replace('  build', str(crayons.yellow('  build')))
    helper = helper.replace('  clean', str(crayons.yellow('  clean')))
    helper = helper.replace('  deploy', str(crayons.green('  deploy')))
    helper = helper.replace('  help', str(crayons.green('  help')))
    helper = helper.replace('  init', str(crayons.blue('  init')))
    helper = helper.replace('  server', str(crayons.green('  server')))
    helper = helper.replace('  new', str(crayons.green('  new')))

    usage_help = USAGE_HELP.format(
        crayons.red('pentoy init'),
        crayons.red('pentoy new'),
        crayons.red('pentoy server'),
        crayons.red('pentoy deploy'),
        crayons.red('pentoy clean')
    )

    helper = helper.replace('Commands:', usage_help)

    return helper


def ensure_python_version():
    """Ensure Python version is 3.x"""
    if get_py_ver() < (3, 3):
        puts(crayons.red('Only Python 3.3+ supported!'), level='warn')
        sys.exit(1)


def ensure_configfile():
    pass


def do_create_project():
    """Create a pentoy project directory."""
    puts(crayons.yellow('Creating new empty site...'), level='info')


def do_init(name=False, ignore_config_file=False):
    """Execute the init functionality."""
    ensure_python_version()
    if not pentoy.project_exists:
        try:
            do_create_project()
        except KeyboardInterrupt:
            sys.exit(1)

    ensure_configfile()

    try:
        root_dir = os.path.dirname(
            pkg_resources.resource_filename(__app__, '__init__'))
        boilerplate = os.path.join(root_dir, 'boilerplate')
        copytree(boilerplate, pentoy.project_path)
    except OSError:
        puts(crayons.red('FileExistsError'), level='warn')

    # shutil.copytree(project.project_path)


def ensure_latest():
    """Update pentoy to latest."""
    try:
        r = requests.get('https://pypi.python.org/pypi/pentoy/json', timeout=1)
    except requests.RequestException as e:
        puts(crayons.red('Failed, {}'.format(e)), level='error')
        sys.exit(1)
    latest = sorted([semver.parse_version_info(v) for v in
                     list(r.json()['releases'].keys())])[-1]
    cur = semver.parse_version_info(__version__)

    if cur < latest:
        import site

        puts('{0}: {1} is available now. Upgrading...'.format(
            crayons.green('Notice'),
            crayons.yellow('Pentoy {v.major}.{v.minor}.{v.patch}'
                           .format(v=latest)),
        ), level='info')

        if site.ENABLE_USER_SITE \
                and site.USER_SITE in sys.modules[__app__].__file__:
            args = ['install', '-U', __app__]
        else:
            args = ['install', '--user', '-U', __app__]

        sys.modules['pip'].main(args)

        puts('{0} to {1}!'.format(
            crayons.green('Pentoy has been updated'),
            crayons.yellow('{v.major}.{v.minor}.{v.patch}'.format(v=latest))
        ), 'info')
    else:
        puts('Already the latest, stay tuned!')


def ensure_project():
    """Ensure current directory is under a pentoy project."""
    pass


def pre_handle(name=None):
    """Pre handle the project."""
    if not name:
        # Handle in current directory.
        if pentoy.project_emtpy:
            puts(crayons.yellow('Creating project {0}.'.format(pentoy.name)))
        else:
            puts('{} not empty, run `pentoy init` on an empty folder.'
                 .format(os.getcwd()), 'warn')
            sys.exit(1)
    else:
        # TODO: Handle in new directory
        project_directory = os.path.join(os.getcwd(), name)
        if os.path.exists(project_directory):
            puts(crayons.red('{0} already exists.'.format(name)), level='warn')
            sys.exit(1)
        else:
            puts(crayons.yellow('Creating project {0}.'.format(pentoy.name)))
            os.mkdir(project_directory)


@click.group(invoke_without_command=True)
@click.option('--help', '-h', is_flag=True, default=None,
              help="Show this message and exit")
@click.option('--update', is_flag=True, default=False, help='Update to latest')
@click.option('--jumbotron', '-j', is_flag=True, default=False, help='Fun.')
@click.version_option(prog_name=crayons.yellow(__app__), version=__version__)
@click.pass_context
def cli(ctx, help=False, update=False, jumbotron=False):
    """
    Pentoy - A light note generator powered by Python.
    """
    if jumbotron:
        puts(crayons.white(xyzzy, bold=True))

    if update:
        ensure_latest()
        sys.exit()
    else:
        pass
        # check_for_updates()

    if ctx.invoked_subcommand is None:
        # Show the help message and exit if no sub-commands followed.
        puts(echo_help(ctx.get_help()))


@cli.command(help='Create an empty pentoy site.')
@click.argument('name', default=False)
def init(name):
    """Create an empty pentoy site with a simple boilerplate"""
    pre_handle(name)
    do_init(name)
    sys.exit(0)


@cli.command(help='Create a new article.')
@click.argument('title')
@click.option('--draft', is_flag=True, default=False, help='Draft mode')
def new(title, draft=False):
    """Create a new post."""
    puts(pentoy.to_json())
    if not title:
        puts('Don\'t forget input the title')
        sys.exit(0)
    if not pentoy.is_under_project:
        puts('Not a pentoy project (or any of the parent directories)', 'warn')
        sys.exit(0)
    date = get_cur_date()
    file_name = date + '-' + format_title(title) + POST_SUFFIX
    full_path = os.path.join(pentoy.post_path, file_name)
    if os.path.exists(os.path.join(pentoy.post_path, file_name)):
        puts('File "%s" already exists, rename the title.' % file_name, 'warn')
        sys.exit(0)

    tpl = pentoy.template_env
    content = tpl.render(title=title, date=date)
    with open(os.path.join(pentoy.post_path, file_name), 'w+') as f:
        f.write(content)
    puts('Created: {}'.format(crayons.green(full_path)))


@cli.command(help='Build your site.')
def build():
    """Build static files."""
    from .builder import Builder

    src_path = pentoy.project_path
    build_path = pentoy.get_default_path()
    puts(build_path)
    rmtree(build_path)

    builder = Builder(src_path, build_path)
    builder.full_build()

    duration = 0
    puts('Start processing')
    puts('Files loaded in %d ms' % duration)


@cli.command(help='Serve your local site.')
@click.option('--port', '-p', type=click.INT, default=None, help='Server port')
@click.option('--browse', '-b', is_flag=True, help='Open the browser')
def serve(port, browse):
    """Serve your site by a local HTTP server for development."""
    project_path = pentoy.project_path
    temp_path = pentoy.get_temp_path()

    puts('Project path: %s' % project_path)
    puts('Temporary path: %s' % temp_path)
    puts('Start processing')
    puts('Pentoy is serving HTTP on http://localhost:{0}/'.format(port))

    from .server import run_server, browse_it
    try:
        run_server('http://127.0.0.1', port, temp_path)
    except Exception as e:
        raise SystemExit(str(e))

    if browse:
        browse_it('http://127.0.0.1', port)


@cli.command(help='Deploy your site.')
@click.option('--github', is_flag=True, help='Deploy to GitHub')
def deploy():
    """Deploy your local site to remote."""
    pass


@cli.command(help='Clear your generated files.')
def clear():
    """Delete all built files."""
    built_path = os.path.join(pentoy.project_path, 'public')
    rmtree(built_path)
    puts('Deleted public folder.')


@cli.command(name='help', help='Seek more details of commands')
@click.argument('cmd')
def help_cmd(cmd):
    puts(crayons.green(cmd))


if __name__ == '__main__':
    cli()
