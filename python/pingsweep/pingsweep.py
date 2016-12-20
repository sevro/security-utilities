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

import pinger 

__author__ = "Derek Goddeau"

_logger = logging.getLogger(__name__)

def main(args):
    """ Main

    TODO: validate ip address input
    
    """
    setup_logs()
    _logger.debug("Starting main()")

    args = parse_args(args)
    if args.a:
        for ip in args.ips:
            print("[*] Scanning class A network {}".format(ip))
    elif args.b:
        for ip in args.ips:
            print("[*] Scanning class B network {}".format(ip))
    elif args.c:
        for ip in args.ips:
            print("[*] Scanning class C network {}".format(ip))
    else:
        main(['-h'])

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
    parser.add_argument(
        '-t',
        '-threads',
        nargs='?',
        type=int,
        default=1,
        const=1,
        help="Number of threads to use",
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
    ``DEBUG`` and write output to ``search.log``. Set console
    handler to default to ``ERROR``.

    """
    logging.basicConfig(level=logging.DEBUG, filename='sweep.log',
                        filemode='w')
    _logger.setLevel(logging.DEBUG)

    # create file handler which logs messages
    fh = logging.FileHandler('search.log')
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
