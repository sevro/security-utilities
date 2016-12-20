# Ping Sweep

Multithreaded ping sweep.

## Usage

Input a list of ip addresses to ping:

	# python pingsweep.py 192.168.1.1 192.168.1.2 192.168.1.3 192.168.1.20
	[*] Scanning list of IP addresses
	192.168.1.1: is alive
	192.168.1.2: is alive
	Network discovered in 2.03591609001 seconds

Specify a type C network and use four threads:

	# python pingsweep.py -t 4 -c 192.168.1.0
	[*] Scanning class C network 192.168.1.0/24
	192.168.1.1: is alive
	192.168.1.2: is alive
	192.168.1.100: is alive
	192.168.1.101: is alive
	192.168.1.125: is alive
	192.168.1.150: is alive
	192.168.1.223: is alive
	Network discovered in 62.5019950867 seconds
