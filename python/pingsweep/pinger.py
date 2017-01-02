#!/usr/bin/python3
# -*- coding: utf-8 -*-
""" pinger.py

Run a fast pingsweep of a given IP range.

"""

from __future__ import division, print_function, absolute_import

import logging
import subprocess
import socket
import re

from Queue import Queue

__author__ = "Derek Goddeau"

_logger = logging.getLogger(__name__)


def icmp_pinger(thread, queue):
    """ Pings given IPs

    """
    while True:
        ip = queue.get()
        result = subprocess.call("ping -c 1 -i 0.2 -W 1 {}".format(ip),
                shell=True,
                stdout=open('/dev/null', 'w'),
                stderr=subprocess.STDOUT)
        if result == 0:
            print("{}".format(ip))
        queue.task_done()


def smtp_pinger(thread, queue):
    """ Checks for open port 25

    If port is open attempts to grab the banner and check for users.
    """
    while True:

        ip = queue.get()
        ports = [25, 465, 587, 2525]

        for port in ports:

            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.2)

            try:
                s.connect((ip, port))
            except (socket.error):
                continue

            port_open = "{} \t port {} open: ".format(ip, port)
            banner = ""

            try:
                banner = s.recv(1024)
                banner = "{}".format(banner.strip())
            except socket.timeout:
                print(port_open, end="")
                print("timeout waiting for banner")
                continue

            users = []      # Found users
            error = False
            usernames = []  # Usernames to try
            usernames = [line.strip() for line in open('usernames.dat')]
            for username in usernames:

                user_result = ""
                try:
                    s.send('VRFY ' + username.lower() + '\r\n')
                    result = s.recv(1024)
                except socket.timeout:
                    break

                if re.match("250", result):
                    users.append(username)
                elif re.match("252", result):
                    pass # User not found
                elif re.match("550", result):
                    break # Not Found
                elif re.match("502", result):
                    error=True
                    error_msg = "\t\t [**] {}: Must use HELO/EHLO first".format(ip)
                    break # Use HELO/EHLO first
                else:
                    error=True
                    error_msg = "\t\t [**] {} Unknown Error: {}".format(ip, result)
                    break

            print(port_open, end="")
            print(banner)
            if error:
                print(error_msg)
            for user in users:
                print("\t\t [**] Found username for {}: {}".format(ip, result))

            s.close()

        queue.task_done()
