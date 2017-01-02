#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" pingsweep.py

Main program for pingsweep.

"""

from __future__ import division, print_function, absolute_import

import argparse
import sys
import logging
import time
import ipaddress

from sweeper import *
from utilities import *

__author__ = "Derek Goddeau"

_logger = logging.getLogger(__name__)

def main(args):
    """ Main

    TODO: validate ip address input
    
    """
    setup_logs()
    _logger.debug("Starting main()")

    ips = []
    args = parse_args(args)
    print("[*] Scanning IP addresses: {}".format(args.ips))
    if args.a:
        ips = get_addresses('a', args.ips)
        if args.ICMP:
            icmp_sweeper(ips, args.threads, 'ICMP')
        elif args.SMTP:
            smtp_sweeper(ips, args.threads, 'SMTP')
    elif args.b:
        ips = get_addresses('b', args.ips)
        if args.ICMP:
            icmp_sweeper(ips, args.threads, 'ICMP')
        elif args.SMTP:
            smtp_sweeper(ips, args.threads, 'SMTP')
    elif args.c:
        ips = get_addresses('c', args.ips)
        if args.ICMP:
            sweeper(ips, args.threads, 'ICMP')
        elif args.SMTP:
            sweeper(ips, args.threads, 'SMTP')
    else:
        if args.ICMP:
            sweeper(args.ips, args.threads, 'ICMP')
        elif args.SMTP:
            sweeper(args.ips, args.threads, 'SMTP')

    _logger.debug("All done, shutting down.")
    logging.shutdown()

def parse_args(args):
    """ Parse command line parameters.

    :return: command line parameters as :obj:`airgparse.Namespace`
    Args:
        args ([str]): List of strings representing the command line arguments.

    Returns:
        argparse.Namespace: Simple object with a readable string
        representation of the argument list.

    """
    parser = argparse.ArgumentParser(
        description="Ping sweep a network to find hosts")
    net_class = parser.add_mutually_exclusive_group()
    scan_type = parser.add_mutually_exclusive_group()
    net_class.add_argument(
        '-a',
        '--a',
        help="Scan a class A network",
        action="store_true")
    net_class.add_argument(
        '-b',
        '--b',
        help="Scan a class B network",
        action="store_true")
    net_class.add_argument(
        '-c',
        '--c',
        help="Scan a class C network",
        action="store_true"),
    scan_type.add_argument(
        '-S',
        '--SMTP',
        help="Scan for SMTP",
        action="store_true"),
    scan_type.add_argument(
        '-I',
        '--ICMP',
        help="Scan IP range for hosts using ICMP",
        action="store_true"),
    parser.add_argument(
        '-t',
        '--threads',
        nargs='?',
        type=int,
        default=1,
        const=1,
        help="Number of threads to use",
        action='store'),
    parser.add_argument(
        '-i',
        '--ip-file',
        nargs='?',
        type=argparse.FileType('r'),
        default="-",
        help="",
        action='store'),
    parser.add_argument(
        '-u',
        '--username-file',
        nargs='?',
        type=argparse.FileType('r'),
        default="-",
        help="",
        action='store'),
    parser.add_argument(
        'ips',
        nargs='+',
        type=str,
        help="List of addresses to scan")
    return parser.parse_args(args)


def setup_logs():
    """ Set up logger to be used between all modules.

    Set logging root and file handler configuration to default to
    ``DEBUG`` and write output to ``sweep.log``. Set console
    handler to default to ``ERROR``.

    """
    logging.basicConfig(level=logging.DEBUG, filename='sweep.log',
                        filemode='w')
    _logger.setLevel(logging.DEBUG)

    # create file handler which logs messages
    fh = logging.FileHandler('sweep.log')
    fh.setLevel(logging.DEBUG)

    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(logging.ERROR)

    # add the handlers to the logger
    _logger.addHandler(fh)
    _logger.addHandler(ch)


if __name__ == "__main__":

    start = time.time()
    main(sys.argv[1:])
    print("Network discovered in {} seconds".format(time.time() - start))
    sys.exit(0)
