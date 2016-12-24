#!/bin/bash
#
# Forward DNS Lookup
# Input: list of subdomains to check, and domain
# Output: subdomains in the input list that exist and their IP address
#
# Example Usage: bash forward_dns.sh common_subdomains.txt megacorpone.com

echo "[*] Scanning $2 for all subdomains listed in $1"
for name in $(cat "$1"); do
    host $name.$2 | grep "has address" | cut -d " " -f 1,4 | tee -a  $2.subdomains.txt
done

sort -u $2.subdomains.txt > tmp && mv tmp $2.subdomains.txt

NUM_SUBDOMAINS=`wc -l $2.subdomains.txt | cut -d " " -f 1`
echo "[*] Found $NUM_SUBDOMAINS subdomains for $2"

exit 0
