#!/bin/bash
#
# Forward DNS Lookup
# Input: list of subdomains to check
# Output: subdomains in the input list that exist and their IP address

for name in $(cat "$1"); do
    host $name.megacorpone.com | grep "has address" | cut -d " " -f 1,4
done
