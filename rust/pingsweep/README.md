# Ping Sweep

Multithreaded ping sweep, port scanning, and SMTP 'VRFY' username checking.

## Usage

From file:

    pingsweep -t 4 file resources/test.dat
    [*] Port [21da:d3:0:2f3b:2aa:ff:fe28:9c5a]:8888 is closed
    [*] Port [::1]:8000 is open
    [*] Port [1200::ab00:1234:2552:7777:1313]:4444 is closed
    [*] Port [1200:0:ab00:1234:0:2552:7777:1313]:1313 is closed
    [*] Port 127.0.0.1:8000 is open
    [*] Port 192.168.1.1:80 is closed
    [*] Port 1.2.3.4:9999 is closed

From list:

    pingsweep -t 4 list 192.168.1.188:80 \[::1\]:2222
    [*] Port [::1]:2222 is closed
    [*] Port 192.168.1.188:80 is closed

