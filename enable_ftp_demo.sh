#!/bin/bash


if [ "$EUID" -ne  0 ]
    then echo "[!!] Please run as root!"
    exit
fi

echo "[+] Installing VSFTP and starting the program..."

yum install vsftpd -y > /dev/null 2>&1

service vsftpd start
