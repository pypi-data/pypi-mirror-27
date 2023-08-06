Python Bash Utils
=================

Author: Tim Santor tsantor@xstudios.agency

Overview
========

Bash color management and log system for Python users.

|Latest Version| |Downloads| |Development Status| |License|

Requirements
============

-  Python 2.7.x, 3.4.x

    NOTE: This has only been tested on a Mac (10.10.2) at this time.

Installation
============

You can install directly via pip:

::

    pip install python-bash-utils

Or from the BitBucket repository (master branch by default):

::

    git clone https://bitbucket.org/tsantor/python-bash-utils
    cd python-bash-utils
    sudo python setup.py install

Usage
=====

colors
------

Import:

::

    from bashutils import colors

Functions:

::

    colors.color_text(text, color="none")

logmsg
------

Import:

::

    from bashutils import logmsg

Functions:

::

    logmsg.log_divline()             # ----------
    logmsg.log_header('header')      # ==> header
    logmsg.log_success('success')    # [✓] success
    logmsg.log_error('error')        # [✗] error
    logmsg.log_warning('warning')    # [!] warning
    logmsg.log_info('info')          # [i] info
    logmsg.log_declined('something') # [✗] something declined. Skipping...

bashutils
---------

Import:

::

    from bashutils import bashutils

Functions:

::

    bashutils.get_os() # OSX, 'Fedora', 'CentOS', 'Debian', 'Ubuntu'

    status, stdout, stderr = bashutils.exec_cmd('git -h')

    bashutils.cmd_exists('git') # True or False

Version History
===============

-  **0.1.0** - Initial release
-  **0.1.1** - Added some new methods
-  **0.1.2** - Refactor
-  **0.1.3** - Added Python 3.4.x support
-  **0.1.4** - Added ability to pass logger instance to log message as
   well
-  **0.1.5** - Added Windows output workaround
-  **0.1.6** - Removed needless ``declined`` method, was being overly
   verbose in output
-  **0.2.0** - Updated for Python 3

Issues
======

If you experience any issues, please create an
`issue <https://bitbucket.org/tsantor/python-bash-utils/issues>`__ on
Bitbucket.

.. |Latest Version| image:: https://pypip.in/version/python-bash-utils/badge.svg
   :target: https://pypi.python.org/pypi/python-bash-utils/
.. |Downloads| image:: https://pypip.in/download/python-bash-utils/badge.svg
   :target: https://pypi.python.org/pypi/python-bash-utils/
.. |Development Status| image:: https://pypip.in/status/python-bash-utils/badge.svg
   :target: https://pypi.python.org/pypi/python-bash-utils/
.. |License| image:: https://pypip.in/license/python-bash-utils/badge.svg
   :target: https://pypi.python.org/pypi/python-bash-utils/
