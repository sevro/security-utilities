# Security Utilities

Useful scripts, see `README.md` files in script directories for individual usage and information.
This project is mirrored to GitHub from the primary repository on GitLab at
[https://gitlab.com/datenstrom/sec-utils](https://gitlab.com/datenstrom/sec-utils) and if
accessed on GitHub may not be the most recent version.

> Legal Disclaimer: usage of tools for attacking web servers without
> prior mutual consistency can be considered as an illegal activity. it is the final user's 
> responsibility to obey all applicable local, state and federal laws. authors assume no 
> liability and are not responsible for any misuse or damage caused by these tools.
>
> Even information gathering such as port scanning is considered illegal in many areas
> and a gery area in most.

## bash

*   [subdom.sh](bash/subdom/): get subdomain information for a webpage
*   [pingsweep.sh](bash/pingsweep/): Ping sweep a class C network
*   [forward_dns.sh](bash/forward_dns/): Run a forward DNS lookup on a domain name for subdomains
*   [reverse_dns.sh](bash/reverse_dns/): Run a reverse DNS lookup on an IP address and given IP range
*   [dns_zonetransfer.sh](bash/dns_zonetransfer/):  Check for DNS server information leakage
*   [port_scan.sh](bash/port_scan/): Scan the full range (1-65355) on list of IPs

## Python

*   [port_check.py](python/port_check/): Check if a single port is open 
*   [pingsweep.py](python/pingsweep/): Multithreaded ping sweep, and port scanning 
*   [fuzzer.py](python/fuzzer/): A fuzzer 
*   [slmail.py](python/SLMail-pwn/): A buffer overflow attack for SLMail 5.5 
*   [vulnserver.py](python/SLMail-pwn/): A buffer overflow attack for the `vulnserver.exe` exercise in OSCP 
*   [crossfire.py](python/crossfire/): A buffer overflow attack for the Crossfire Linux game

## C

*   [slmail-linux.c](c/slmail-linux/): A buffer overflow attack for SLMail 5.5 compiled for Linux
*   [slmail-windows.c](c/slmail-windows/): A buffer overflow attack for SLMail 5.5 compiled for Windows 

## FTP

It is possible to turn FTP into a non-interactive process by providing the Windows
default FTP client `ftp.exe` with a text file containing FTP commands. This is
useful in _post exploitation_ when there is a need to upload files and tools to a
machine.

*   [setup-ftp.sh](ftp/pureFTPd/): Install and configure a FTP server on (Debian like) Linux

## Note on extension convention

All program output files are by convention use the `.txt` extension which are ignored by the
`.gitignore`. All files for input are by convention `.dat` which will be tracked.
