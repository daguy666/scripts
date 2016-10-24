#!/usr/bin/env python
# -----------------------------------------------------------
# Filename      : get_httpd_verbs.py
# Created By    : Joe Pistone
# Date Created  : 24-Oct-2016 18:16
# Date Modified :
#------------------------------------------------------------
# License       : Development
#------------------------------------------------------------
# Description   : Returns the HTTP verbs a webserver is serving
#------------------------------------------------------------
# (c) Copyright 2016, TheKillingTime all rights reserved.
#------------------------------------------------------------
# This command line tool might be useful for enumerating 
# misconfigured  webservers. You can scan a single host or 
# an ip range using CIDR notation. Run responsibly and at 
# your own risk
#------------------------------------------------------------

import os
import sys
import socket
import httplib
import netaddr


class Get_HTTP_Options(object):
    
    def __init__(self):
        self.scan_type = scan_type
        self.range_or_host = host_hosts

    def options_request(self, hostname):
        """
        This method makes the option request
        """
        try:
            conn = httplib.HTTPConnection(hostname, timeout=1)
            conn.request('OPTIONS', '/')
            response = conn.getresponse()
            return response.getheader('allow')
        except socket.error:
            return "[!] Connection Refused or host is down."

    def ip_range_scan(self):
        """
        This method will allow the operator to scan a range using
        CIDR notation.
        """
        try:
            for ip in netaddr.IPNetwork(self.range_or_host):
                print "==" * 25
                print "Checking Host: %s " % str(ip)
                print "%s" % self.options_request(str(ip))
            print "==" * 25
        except netaddr.core.AddrFormatError:
            print "[!] Invalid Network Range." 

    def single_host_scan(self):
        """
        This method allows the operator scan a single host
        """
        print "==" * 25 
        print "Checking Host: %s " % str(self.range_or_host)
        print "%s" % self.options_request(self.range_or_host)
        print "==" * 25 

if __name__ == '__main__':

    # help / usage info
    usage = """[?] Usage:
            To scan a single host: 
            %s (-h or --hostname) (hostname)

            To scan an ip range:
            %s (-r or --range) (ip range)

            --help or ? to print this help. 
            """ % (sys.argv[0], sys.argv[0])

    try:
        # Validate the length of sys.argv
        if len(sys.argv) != 3:
            print usage
            sys.exit(1)
        
        # Setup some vars for operators scan type and host(s)
        scan_type = sys.argv[1].lower()
        host_hosts = sys.argv[2]

        # Parse out a range of ips to scan
        if scan_type  == '--range' or scan_type == '-r':
           gho = Get_HTTP_Options()
           gho.ip_range_scan()

        # Parse out a single host to scan  
        elif scan_type == '--host' or scan_type == '-h':
            gho = Get_HTTP_Options()
            gho.single_host_scan()
        
        # HALP
        elif scan_type == '-?' or scan_type == '?' or scan_type  == '--help':
            print usage
            sys.exit(1)

        # If all else fails
        else:
            print "[!] Invalid Scan Type. Please use range or host"

    except KeyboardInterrupt:
        print "\n[-] Exited Program."
