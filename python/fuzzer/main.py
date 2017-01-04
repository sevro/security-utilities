#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" main.py

Main program for fuzzer.

"""

from __future__ import division, print_function, absolute_import

import argparse
import sys
import logging
import time

from fuzzer import fuzz

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
    print("[*] Fuzzing port {} on IP address {}".format(args.port, args.ip))
    fuzz(args.ip, args.port, args.size, args.increment)

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
        description="A fuzzer")
    parser.add_argument(
        '-s',
        '--size',
        type=int,
        default=6000,
        help="Maximum size of buffers in bytes"),
    parser.add_argument(
        '-i',
        '--increment',
        nargs='?',
        type=int,
        default=200,
        help="Amount to increment the buffer size"),
    parser.add_argument(
        '-p',
        '--port',
        nargs='+',
        type=int,
        help="Port to connect to"),
    parser.add_argument(
        'ip',
        type=str,
        help="IP address to connect to")
    return parser.parse_args(args)


def setup_logs():
    """ Set up logger to be used between all modules.

    Set logging root and file handler configuration to default to
    ``DEBUG`` and write output to ``fuzz.log``. Set console
    handler to default to ``ERROR``.

    """
    logging.basicConfig(level=logging.DEBUG, filename='fuzz.log',
                        filemode='w')
    _logger.setLevel(logging.DEBUG)

    # create file handler which logs messages
    fh = logging.FileHandler('fuzz.log')
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
    print("Fuzzer completed in {} seconds".format(time.time() - start))
    sys.exit(0)
