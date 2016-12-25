#!/bin/bash
if [ "$1" == "" ]
then
    echo "Usage: ./port_scan.sh <file>"
    echo "Example: ./port_scan.sh my_ip_list.txt"
else
    mkdir -p target
    for ip in $(cat "$1"); do
        echo "[*] Scanning ip address $ip"
        nmap -nsSU -A -sV --version-all $ip -p 1-65355 > target/portscan.$ip.txt &
        pid="$!"
        wait $pid || let "RESULT=1"
        if [ "$RESULT" == "1" ]; then
            echo "[*] It blew up"
            exit 1
        fi
    done
fi
exit 0
