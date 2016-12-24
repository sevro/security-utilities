#!/bin/bash
#
# Reverse DNS Lookup
# Input: An IP address, a range, and a filter
# Output: 
#
# Example Usage: bash reverse_dns.sh [ip address] [range start] [range stop] [filter]
#                bash reverse_dns.sh 38.100.193 72 91 megacorp

echo "[*] Scanning $1 in range $2 to $3"
for ip in $(seq "$2" "$3"); do
    host $1.$ip | grep "$4" | cut -d " " -f 1,5 | tee -a  $1.subdomains.txt
done
echo "[*] filtered all domains without the string $4"

sort -u $2.subdomains.txt > tmp && mv tmp $2.subdomains.txt

NUM_SUBDOMAINS=`wc -l $2.subdomains.txt | cut -d " " -f 1`
echo "[*] Found $NUM_SUBDOMAINS subdomains for $1"

exit 0
