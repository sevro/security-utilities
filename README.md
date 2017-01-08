# Security Utilities

Useful scripts, see `README.md` files in script directories for usage and information.

> Legal Disclaimer: usage of tools for attacking web servers without
> prior mutual consistency can be considered as an illegal activity. it is the final user's 
> responsibility to obey all applicable local, state and federal laws. authors assume no 
> liability and are not responsible for any misuse or damage caused by these tools.
>
> Even information gathering such as port scanning is considered illegal in many areas
> and a gery area in most.

## bash

*   `subdom.sh`: get subdomain information for a webpage [README](bash/subdom/README.md)
*   `pingsweep.sh`: Ping sweep a class C network [README](bash/pingsweep/README.md)
*   `forward_dns.sh`: Run a forward DNS lookup on a domain name for subdomains [README](bash/forward_dns/README.md)
*   `reverse_dns.sh`: Run a reverse DNS lookup on an IP address and given IP range [README](bash/reverse_dns/README.md)
*   `dns_zonetransfer.sh`:  Check for DNS server information leakage [README](bash/dns_zonetransfer/README.md)
*   `port_scan.sh`: Scan the full range (1-65355) on list of IPs [README](bash/port_scan/README.md)

## Python

*   `port_check.py`: Check if a single port is open [README](python/port_check/README.md) 
*   `pingsweep.py`: Multithreaded ping sweep, and port scanning [README](python/pingsweep/README.md) 
*   `fuzzer.py`: A fuzzer [README](python/fuzzer/README.md) 
*   `slmail.py`: A buffer overflow attack for SLMail 5.5 [README](python/SLMail-pwn/README.md) 
*   `vulnserver.py`: A buffer overflow attack for the `vulnserver.exe` exercise in OSCP [README](python/SLMail-pwn/README.md) 
*   `crossfire.py`: A buffer overflow attack for the Crossfire Linux game [README](python/crossfire/README.md) 

## C

*   `slmail-linux.c`: A buffer overflow attack for SLMail 5.5 compiled for Linux [README](c/slmail-linux/README.md) 
*   `slmail-windows.c`: A buffer overflow attack for SLMail 5.5 compiled for Windows [README](c/slmail-windows/README.md) 

## Note

All program output files are by convention use the `.txt.` extension which are ignored by the
`.gitignore`. All files for input are by convention `.dat` which will be tracked.
