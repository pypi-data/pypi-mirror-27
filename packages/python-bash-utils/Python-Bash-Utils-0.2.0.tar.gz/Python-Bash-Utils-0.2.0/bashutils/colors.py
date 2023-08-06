# -- coding: utf-8 --

# Copyright 2015
#
# This file is part of proprietary software and use of this file
# is strictly prohibited without written consent.
#
# @author  Tim Santor  <tsantor@xstudios.agency>

"""Helps outputting colored text to the console."""

from __future__ import absolute_import, print_function, unicode_literals
import platform

# -----------------------------------------------------------------------------

COLOR_CODES = {
    'none': '\033[39m',
    'red': '\033[91m',
    'green': '\033[92m',
    'yellow': '\033[93m',
    'blue': '\033[94m',
    'magenta': '\033[95m',
    'cyan': '\033[96m',
    'white': '\033[97m',
    'grey': '\033[37m',
}

COLOR_RESET = '\033[0m'

# -----------------------------------------------------------------------------


def get_color(color):
    """Returns a color from the COLOR_CODES."""
    key = color.lower()
    if key not in list(COLOR_CODES.keys()):
        key = "none"

    return COLOR_CODES[key]


def color_text(text, color="none"):
    """Returns colored text"""
    if platform.system() in ['Windows', 'Win32', 'Win64']:
        return text
    color = get_color(color)
    return color + text + COLOR_RESET

# -----------------------------------------------------------------------------

if __name__ == "__main__":
    print(color_text('red', 'RED'))
    print(color_text('green', 'GREEN'))
    print(color_text('yellow', 'YELLOW'))
    print(color_text('blue', 'BLUE'))
    print(color_text('magenta', 'MAGENTA'))
    print(color_text('cyan', 'CYAN'))
    print(color_text('white', 'WHITE'))
    print(color_text('grey', 'GREY'))

    print(color_text('invalid', 'INVALID'))
    print(color_text('none'))
