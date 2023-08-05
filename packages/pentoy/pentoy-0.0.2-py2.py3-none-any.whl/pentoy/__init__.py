#  __________               __
#  \______   \ ____   _____/  |_  ____ ___.__.
#   |     ___// __ \ /    \   __\/  _ <   |  |
#   |    |   \  ___/|   |  \  | (  <_> )___  |
#   |____|    \___  >___|  /__|  \____// ____|
#                 \/     \/            \/

import sys

if sys.version_info < (3, 3):
    sys.stderr.write("WARNING: Python 3.3+ supported only!")

__app__ = 'pentoy'
__author__ = 'sudoz'

from .cli import cli

if __name__ == '__main__':
    cli()
