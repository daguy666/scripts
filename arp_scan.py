#!/usr/bin/env python
# -----------------------------------------------------------
# Filename      : arp_scan.py
# Created By    : Joe Pistone
# Date Created  : 18-Sept-2016 18:16
# Date Modified :
#------------------------------------------------------------
# License       : Development
#
# Description   : Network Discovery tool
#
# (c) Copyright 2015, TheKillingTime all rights reserved.
#-----------------------------------------------------------

__author__  = "Joe Pistone"
__version__ = "1.0"

import os
import socket
import netaddr
import logging
# Setup logging for scapy to run at Error level.
logging.getLogger('scapy.runtime').setLevel(logging.ERROR)
from scapy.all import *
from netaddr import EUI, OUI, IPNetwork


# Cleans up Scapy's mess a little bit.
conf.verb=0


class Scan_Network(object):

    def __init__(self, ip_range):
        self.ip_range = ip_range

 
    def hardware_vendor(self, mac):
         """This function will take a mac address
            The pull out the oui and analyze it.
         """
         try:
             hw_id = EUI(mac)
             oui = hw_id.oui
             return oui.registration().org 
         except netaddr.NotRegisteredError, err:
             return "NA"

    def get_hostname(self, ip):
        try:        
            return socket.gethostbyaddr(str(ip))[0]
        except socket.gaierror:
            return "NA"
        except socket.herror:
            return "NA"

    def get_macs(self):
        print "--" * 25
        print "Analyzing Network, Please wait..."
        print "--" * 25
        for ip in netaddr.IPNetwork(self.ip_range):
            ans, unans = srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=str(ip)), timeout=2)
            for s, r in ans:
                print "[>] Hostname: %s => IP Address: %s => Mac Address: %s => Vendor: %s" % \
                      (self.get_hostname(str(ip)), str(ip), str(r.src), self.hardware_vendor(r.src))

        print "--" * 25

    def main(self):
        self.get_macs()

if __name__ == '__main__':
    if os.getuid() != 0:
        print "[!] Please run as root."
        sys.exit(1)

    if len(sys.argv) != 2:
        print "[!] Usage %s CIDR range <192.168.1.1/24>"
        sys.exit(1)
    
    if sys.argv[1].lower() == 'y':
        ip_range = '192.168.1.1/24'
    else:
        ip_range = sys.argv[1]

    try:
        net_scan = Scan_Network(ip_range)
        net_scan.main()
    except KeyboardInterrupt:
        print "\n[-] Program Exited."
