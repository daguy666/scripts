#!/bin/bash


if [ "$EUID" -ne 0 ]
    then echo "[!!] Please run as root!"
    exit
fi

echo "[-] Stopping VSFTP and uninstalling the program..."

service vsftpd stop
yum erase vsftpd -y /dev/null > 2>&1

echo "[-] VSFTPd has been removed."
