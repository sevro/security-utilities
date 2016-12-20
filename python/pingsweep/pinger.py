#!/usr/bin/python3
# -*- coding: utf-8 -*-
""" pinger.py

Run a fast pingsweep of a given IP range.

"""

from __future__ import division, print_function, absolute_import

import logging
import ipaddress
from subprocess import Popen

__author__ = "Derek Goddeau"

_logger = logging.getLogger(__name__)


def pinger(net_class, ipaddress):
    """ Ping subnet

    """
    if net_class == 'a':
        ipv4 = ipaddress.ip_network("{}/24".format(ipaddress))
    elif net_class == 'b':
        ipv4 = ipaddress.ip_network("{}/24".format(ipaddress))
    elif net_class == 'c':
        ipv4 = ipaddress.ip_network("{}/24".format(ipaddress))
    else:
        # ping the ip
        pass
