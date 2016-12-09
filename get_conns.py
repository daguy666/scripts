#!/usr/bin/env python

import os
import re
import sys
import psutil
import platform

from pprint import pprint

'''
sconn(fd=-1, family=2, type=1, laddr=('0.0.0.0', 22), raddr=(), status='LISTEN', pid=None)
sconn(fd=-1, family=2, type=1, laddr=('0.0.0.0', 22), raddr=('0.0.0.0', 59162), status='ESTABLISHED', pid=None)
sconn(fd=-1, family=2, type=2, laddr=('0.0.0.0', 5355), raddr=(), status='NONE', pid=None)
sconn(fd=-1, family=2, type=1, laddr=('0.0.0.0', 56375), raddr=(), status='LISTEN', pid=None)
'''

class Matching_Things(object):

    def ip_v6(self, ok):
        # Match IP_V6
        if re.match(r"^(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(ffff(:0{1,4}){0,1}:){0,1}((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9]))", ok):
            return True
        else:
            return False

    def mac_address(self, ok):
        # Match mac address
        if re.match(r"^([0-9a-fA-F][0-9a-fA-F][:-]){5}([0-9a-fA-F][0-9a-fA-F])$", ok):
            return True
        else:
            return False

    def ip_v4(self, ok):
        # Match IP_V4
        if re.match(r"^((25[0-5]|2[0-5][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$", ok):
            return True
        else:
            return False

class Get_Interface_Addresses(object):
    
    def __init__(self):
        self.interface_info = psutil.net_if_addrs()
        self.interface_name_list = []
        self.match = Matching_Things()
    
    def gather_interface_info(self):
        """
        Take all the interface names and append
        them to a list.
        """
        for int_name in self.interface_info:
            #self.interface_name_list.append(int_name)
            for i in self.interface_info[int_name]:
                if self.match.mac_address(i.address):
                    address = "HW Address: %s" % i.address
                elif self.match.ip_v4(i.address):
                    address = "IP: %s" % i.address
                elif self.match.ip_v6(i.address):
                    address = "IPV6: %s" % i.address
                else:
                    address = "Address: %s " % i.address
                print "Interface: %s => %s => Netmask: %s" % (int_name, address, i.netmask)
    
    def main(self):
        print "--" * 25
        print "Interface Info"
        print "--" * 25
        self.gather_interface_info()
        print "--" * 25

class Get_Connection_Info(object):

    def __init__(self):
        self.connections = psutil.net_connections()

    def check_for_established(self):
        """
        Checks for established connections.
        """
        for i in self.connections:
            if i.status == 'ESTABLISHED':
                local_address = "Server IP: %s" % i.laddr[0]
                local_port = "PORT: %d" % i.laddr[1]
                remote_address = "Cient IP: %s" % i.raddr[0]
                print "%s => %s => %s" % (local_address, local_port, remote_address)
        #print "--" * 25

    def check_for_listen(self):
        """
        Checks for listening ports.
        """
        for i in self.connections:
            if i.status == 'LISTEN':
                listen_ip = "IP: %s" % i.laddr[0]
                listen_port = "Port: %d" % i.laddr[1]
                print "%s => %s" % (listen_ip, listen_port)
        #print "--" * 25

    def print_output(self, conn_type):
        """
        Prints the output to the screen.
        """
        print "--" * 25
        print "%s Connections" % conn_type
        print "--" * 25


    def main(self):
        self.print_output('Established')
        self.check_for_established()
        self.print_output('Listening')
        self.check_for_listen()


if __name__ == '__main__':
    if platform.mac_ver()[0]: 
        if os.getuid() != 0:
            print "[!] Please run as root on OSX."
            sys.exit(1)
    gci = Get_Connection_Info()
    gci.main()
    gia = Get_Interface_Addresses()
    gia.main()
