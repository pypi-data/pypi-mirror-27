# -- coding: utf-8 --

# Copyright 2015
#
# This file is part of proprietary software and use of this file
# is strictly prohibited without written consent.
#
# @author  Tim Santor  <tsantor@xstudios.agency>

"""Ouptuts formatted, colored log messages to the console."""

# -----------------------------------------------------------------------------

from __future__ import absolute_import, print_function, unicode_literals

import codecs
import sys

from six.moves import input

from .bashutils import get_os
from .colors import color_text

# Use consistent encoding for terminal?
# http://chase-seibert.github.io/blog/2014/01/12/python-unicode-console-output.html
sys.stdout = codecs.getwriter('utf8')(sys.stdout)
sys.stderr = codecs.getwriter('utf8')(sys.stderr)

# -----------------------------------------------------------------------------
# User feedback
# -----------------------------------------------------------------------------


def divline():
    """Prints a divider line."""
    print('-' * 80)


def header(string, logger=None):
    """Prints a header."""
    if logger:
        logger.info(string)
    value = color_text('==> ', 'green') + color_text(string, 'white')
    print(value)
    return value


def subheader(string, logger=None):
    """Prints a subheader."""
    if logger:
        logger.info(string)
    value = color_text('==> ', 'blue') + string
    print(value)
    return value


def success(string, logger=None):
    """Prints a success message."""
    if logger:
        logger.info(string)
    if get_os() == 'Windows':
        value = '[+] ' + string
    else:
        value = color_text('[✓] ', 'green') + string
    print(value)
    return value


def error(string, logger=None):
    """Prints a error message."""
    if logger:
        logger.error(string)
    if get_os() == 'Windows':
        value = '[x] ' + string
    else:
        value = color_text('[✗] ', 'red') + string
    print(value)
    return value


def warning(string, logger=None):
    """Prints a warning message."""
    if logger:
        logger.warning(string)
    if get_os() == 'Windows':
        value = '[!] ' + string
    else:
        value = color_text('[!] ', 'yellow') + string
    print(value)
    return value


def info(string, logger=None):
    """Prints a info message."""
    if logger:
        logger.info(string)
    value = color_text('[i] ', 'cyan') + string
    print(value)
    return value

# For backwards compatibility as we renamed our methods
log_divline = divline
log_header = header
log_success = success
log_error = error
log_warning = warning
log_info = info

# -----------------------------------------------------------------------------
# User Input
# -----------------------------------------------------------------------------


def prompt(question):
    """Prompts user for input."""
    # Python 2to3 compatbility
    response = input(color_text('[?] ', 'yellow') +
                     color_text(question, 'cyan') + ' ')
    return response


def confirm(question):
    """Prompts user to confirm with (y/n)."""
    # Python 2to3 compatbility
    response = input(color_text('[?] ', 'yellow') +
                     color_text(question, 'cyan') + '? (y/n) ')

    if response in ['y', 'yes']:
        return True
    return False

# -----------------------------------------------------------------------------

if __name__ == "__main__":
    divline()
    header('header')
    success('success')
    error('error')
    warning('warning')
    info('info')

    print(prompt('What is your name?'))

    if confirm('Confirm this'):
        print('You confirmed!')
