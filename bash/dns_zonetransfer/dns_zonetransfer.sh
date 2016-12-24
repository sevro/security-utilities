#!/bin/bash
#
# DNS Zone Transfer
# Input: Domain Name
# Output: All DNS domains and IP addresses on success
#
# Example Usage: bash dns_zonetransfer.sh megacorpone.com

if [ -z "$1" ]; then
    echo "[*] Zone Transfer script"
    echo "[*] Usage : $0 <domain name>"
    exit 0
fi

echo "[*] Checking $1 for zone transfers"
echo "[*] Found DNS servers:"
host -t ns $1 | cut -d " " -f 4 | tee dns_servers.txt

for server in $(cat "dns_servers.txt"); do
    echo "[*] Checking DNS server: $server"
    host -l $1 $server | grep "has address" | tee -a zone_transfers.txt
done

exit 0
