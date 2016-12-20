#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" sweeper.py

The network sweep logic.

"""

from __future__ import division, print_function, absolute_import

import logging

from Queue import Queue
from threading import Thread

import pinger

__author__ = "Derek Goddeau"

_logger = logging.getLogger(__name__)

def sweeper(ips, threads):
    """ Start threads, put ips in queue 

    """
    queue = Queue()
    for thread_id in range(threads):
	worker = Thread(target=pinger.pinger, args=(thread_id, queue))
	worker.setDaemon(True)
	worker.start()
    for ip in ips:
	queue.put(ip)
    queue.join()
