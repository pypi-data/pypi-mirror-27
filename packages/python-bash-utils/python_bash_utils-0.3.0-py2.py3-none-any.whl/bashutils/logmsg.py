# -- coding: utf-8 --

"""Ouptuts formatted, colored log messages to the console."""

from __future__ import absolute_import, print_function, unicode_literals

from colorama import Fore, init as colorama_init

from six.moves import input

colorama_init(autoreset=True)

# -----------------------------------------------------------------------------
# User feedback
# -----------------------------------------------------------------------------


def divline():
    """Prints a divider line."""
    print('-' * 80)


def header(string):
    """Prints a header."""
    value = Fore.WHITE + '==> ' + string
    print(value)
    return value


def success(string):
    """Prints a success message."""
    value = Fore.GREEN + '[+] ' + string
    print(value)
    return value


def error(string):
    """Prints a error message."""
    value = Fore.RED + '[-] ' + string
    print(value)
    return value


def warning(string):
    """Prints a warning message."""
    value = Fore.YELLOW + '[!] ' + string
    print(value)
    return value


def info(string):
    """Prints a info message."""
    value = Fore.CYAN + '[i] ' + string
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
    response = input('[?] {} '.format(question))
    return response


def confirm(question):
    """Prompts user to confirm with (y/n)."""
    # Python 2to3 compatbility
    response = input('[?] {}? (y/n) '.format(question))

    if response in ['y', 'yes']:
        return True
    return False

# -----------------------------------------------------------------------------

if __name__ == "__main__":
    divline()
    header('Header')
    success('Success')
    error('Error')
    warning('Warning')
    info('Info')

    name = prompt('What is your name?')
    print(name)

    if confirm('Confirm this'):
        print('You confirmed!')
