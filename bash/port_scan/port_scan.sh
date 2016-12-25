#!/bin/bash
if [ "$1" == "" ]
then
    echo "Usage: ./port_scan.sh <file>"
    echo "Example: ./port_scan.sh my_ip_list.txt"
else
    mkdir -p target
    for ip in $(cat "$1"); do
        nmap -nsSU $ip -p 1-65355 > target/portscan.$ip.txt &
        pid="$!"
        wait $pid || let "RESULT=1"
        if [ "$RESULT" == "1" ]; then
            exit 1
        fi
    done
fi
exit 0
