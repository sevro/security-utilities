#!/bin/bash

WGET_OPTS="--show-progress --random-wait --restrict-file-names=unix"
TARGET_DIR="tmp/"
EXISTING_FILES_DIR="tmp/"

############
# Validate #
############

if [ "$#" -ne 1 ]; then
    echo "[*] ERROR: Incorrect number of parameters. Aborting..." >&2
    echo "Usage: bash $0 [domain]" >&2
    exit 1
elif ! curl -s --head $1 | head -n 1 | grep "HTTP/1.[01] [23].."; then
    echo "[*] ERROR: input is not a valid domain name. Aborting..." >&2
    echo "Usage: bash $0 [domain]" >&2
    exit 1
elif ! command -v wget >/dev/null 2>&1 ; then
    echo "[*] ERROR: I require wget but it's not installed.  Aborting..." >&2
    exit 1
fi


############
# Clean up #
############

# Delete each file in a loop.
for file in "$EXISTING_FILES_DIR"/*; do
    rm -f "$file"
done

truncate -s 0 url_list.txt
truncate -s 0 host_list.txt
truncate -s 0 ip_list.txt

############
# Execute  #
############

if ! wget --directory-prefix="$TARGET_DIR" ${WGET_OPTS} "$1"; then
    echo "ERROR: can't fetch webpage. Aborting..." >&2
    exit 1
else

    # Get all urls from page
    for file in "$TARGET_DIR"/*; do
        cat "$file" | grep -o 'http://[^"]*' | cut -d "/" -f 3 >> url_list.txt
    done
    sort -u "url_list.txt" | tee url_list.txt

    # Get host info for all urls
    for url in $(cat url_list.txt); do
        host "$url" | grep "has address" | tee -a host_list.txt | cut -d " " -f 4 >> ip_list.txt
    done
    sort -u "host_list.txt" | tee host_list.txt
    sort -u "ip_list.txt" | tee ip_list.txt
fi

exit 0
