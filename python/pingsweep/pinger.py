#!/usr/bin/python3
# -*- coding: utf-8 -*-
""" pinger.py

Run a fast pingsweep of a given IP range.

"""

from __future__ import division, print_function, absolute_import

import logging
import subprocess
from Queue import Queue

__author__ = "Derek Goddeau"

_logger = logging.getLogger(__name__)


def pinger(thread, queue):
    """ Pings given IPs

    """
    while True:
        ip = queue.get()
        result = subprocess.call("ping -c 1 -i 0.2 -W 1 {}".format(ip),
                shell=True,
                stdout=open('/dev/null', 'w'),
                stderr=subprocess.STDOUT)
        if result == 0:
            print("{}: is alive".format(ip))
        queue.task_done()
