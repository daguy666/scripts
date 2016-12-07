#!/usr/bin/env python

import os
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

class Get_Interface_Addresses(object):
    
    def __init__(self):
        self.interface_info = psutil.net_if_addrs()
        self.interface_name_list = []
    
    def gather_interface_info(self):
        """
        Take all the interface names and append
        them to a list.
        """
        for int_name in self.interface_info:
            #self.interface_name_list.append(int_name)
            for i in self.interface_info[int_name]:
                print "Interface: %s => IP: %s => Netmask: %s" % (int_name, i.address, i.netmask)


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
