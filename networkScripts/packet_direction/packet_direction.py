#!/usr/bin/env python

import sys
import logging
# Cleans up a little of scapy's run time mess.
logging.getLogger('scapy.runtime').setLevel(logging.ERROR)
import pygeoip
import proto_to_numbers
from scapy.all import *

# Moar scapy clean up
conf.verb=0


class Inspect_Traffic(object):

    def __init__(self):
        # MaxMind GeoIP database
        self.geodb = '/usr/local/geo/GeoLiteCity.dat'
        self.count = 1000
        print "Capturing %d packets ..." % self.count
        # Sniff some packets!
        self.packets = sniff(iface="en0", count=self.count)
        


    def geo_lookup(self, ip_address):
        """This method will do a geo lookup
           against an ip address.
        """
        try:
            gic = pygeoip.GeoIP(self.geodb)

        except IOError:
            print "Cannot open %s." % self.geodb
            sys.exit(1)

        try:
            geo_json = gic.record_by_addr(ip_address)
            output = geo_json['country_code']

        except:
            output = "Unregistered"

        return output

    def parse_scapy_ness(self):
        """This method should parse the output
           from the packet capture.
        """
        for packet in self.packets[IP]:
            # Geo look-ups on source and dest.
            src_geo = self.geo_lookup(str(packet[0][IP].src))
            dst_geo = self.geo_lookup(str(packet[0][IP].dst))

            self.source = "Source: %s Location: %s ==>" % (packet[0][IP].src, src_geo)
            self.dest   = "Destination: %s Location: %s " % (packet[0][IP].dst, dst_geo)

            proto_2_num = str(packet[0][IP].proto)
            self.proto  = "[+] Protocol: %s " % proto_to_numbers.protocols[proto_2_num]
            self.value = " ".join([self.proto, self.source, self.dest])
            print self.value



    def main(self):
        print "Capturing some packets to inspect ..."
        self.parse_scapy_ness()




if __name__ == '__main__':
    inspect = Inspect_Traffic()
    inspect.main()

#TODO incorporate the geo lookup in the parse method
#TODO add some error handling around the ip look up in case its a private ip.
