#!/bin/bash

for i in `fdesetup list | awk -F , '{print $1}' | grep -vi itsupport` ; do
    fdesetup remove -user $i ;
done

/sbin/reboot
