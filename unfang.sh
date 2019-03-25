#!/bin/sh
# =========================================================
# This is a tool that will refang an IOC.
# A safe IOC is defanged, and not clickable.
# This tool will convert a defanged list of
# IOCs to fanged. For importing into another tool.
# =========================================================



if [ -z "$1" ]
then
    echo "[!] Usage ./unfang.sh </path/to/file>"
    exit 1
fi

/usr/bin/sed 's/\[\.\]/./g' "$1"
