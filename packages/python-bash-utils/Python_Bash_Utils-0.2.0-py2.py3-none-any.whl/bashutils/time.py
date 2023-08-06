# -- coding: utf-8 --

# Copyright 2016
#
# This file is part of proprietary software and use of this file
# is strictly prohibited without written consent.
#
# @author  Tim Santor  <tsantor@xstudios.agency>

"""Time methods for aiding in timing execution."""

# -----------------------------------------------------------------------------

from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import time
import datetime

# -----------------------------------------------------------------------------


def secs_to_mins(seconds):
    """Converts seconds to minutes."""
    # m, s = divmod(seconds, 60)
    # h, m = divmod(m, 60)
    # return '%d:%02d:%02d' % (h, m, s)
    return str(datetime.timedelta(seconds=seconds))


class Timer(object):
    """Timer to simplify timing of execution."""

    def start(self):
        self.start_time = time.time()
        return self

    def stop(self):
        self.end_time = time.time()
        return self

    def elapsed(self):
        return secs_to_mins(self.end_time - self.start_time)
        return self
