#!/usr/bin/env python

import os
from scapy.all import *

def arp_callback(packet):
    if packet[ARP].op == 1:
	print "Request: %s is asking about %s" % (str(packet[ARP].prsc), str(packet[ARP].pdst))
    if packet[ARP].op == 2:
	print "Request: %s has address %s" % (str(packet[ARP].hwsrc), str(packet[ARP].prsc))


if __name__ == '__main__':
    try:
	if os.getuid() == 0:
	    sniff(prn=arp_callback,filter="arp", store=0)
    except Exception, err:
	print "Error: %s" % err
