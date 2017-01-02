#!/bin/bash
if [ "$1" == "" ]
then
    echo "Usage: ./port_scan.sh <file>"
    echo "Example: ./port_scan.sh my_ip_list.txt"
else
    mkdir -p target
    for ip in $(cat "$1"); do
        echo "[*] Scanning ip address $ip"
        nmap -nsSU -A -sV --version-all --stats-every 120s --host-timeout 30m -T3 $ip -p 1-65355 | tee target/portscan.$ip.txt
    done
fi
exit 0
