#!/usr/bin/python3
# -*- coding: utf-8 -*-
""" pinger.py

Run a fast pingsweep of a given IP range.

"""

from __future__ import division, print_function, absolute_import

import logging
import ipaddress

__author__ = "Derek Goddeau"

_logger = logging.getLogger(__name__)


def get_addresses(network_type, ips):
    """ A network type generate a list of ip addresses

    """
    ip_strlist = []
    for ip in ips:
        if network_type == 'a':
            print("[*] Expanding address into a class A network: {}/8".format(ip))
            ip_range = ipaddress.ip_network(u'{}/8'.format(ip))
            ip_list = list(ip_range)
            for ipaddr in ip_list:
                ipaddr = str(ipaddr)
                ip_strlist.append(ipaddr)
        if network_type == 'b':
            print("[*] Expanding address into a class B network: {}/16".format(ip))
            ip_range = ipaddress.ip_network(u'{}/16'.format(ip))
            ip_list = list(ip_range)
            for ipaddr in ip_list:
                ipaddr = str(ipaddr)
                ip_strlist.append(ipaddr)
        if network_type == 'c':
            print("[*] Expanding address into a class C network: {}/24".format(ip))
            ip_range = ipaddress.ip_network(u'{}/24'.format(ip))
            ip_list = list(ip_range)
            for ipaddr in ip_list:
                ipaddr = str(ipaddr)
                ip_strlist.append(ipaddr)
        return ip_strlist
