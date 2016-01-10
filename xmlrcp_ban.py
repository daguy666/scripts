#!/usr/bin/env python

import os
import sys
import subprocess
from datetime import datetime


class Block_Xmlrpc(object):

    def __init__(self):
        self.wp_log     = "/var/log/httpd/wordpress-acces-log"
        self.xmlrpc_log = "/var/log/xmlrpc/xmlrpc.log"
        self.ban_log    = "/var/log/xmlrpc/xmlrpc_ban.log"
        self.ip_list    = []
        self.timestamp  = datetime.now()

    def shell_cmd(self, cmd):
        """Runs a shady ass shell command.
        """
        cmd_ex = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        output = cmd_ex.communicate()[0]

    def grab_ips(self):
        """Parses a log file and grabs the ip address
           from it.
        """
        parse_log = open(self.xmlrpc_log, 'r')
        for entry in parse_log:
            just_ip = entry.split()
            ip = just_ip[0]
            self.ip_list.append(ip)
        ip_set = set(self.ip_list)
        ips = list(ip_set)
        return ips

    def write_ban_log(self, log_line):
        with open(self.ban_log, 'a') as banned:
            banned.write(log_line)

    def main(self):
        grp_cmd    = "grep -iE '(POST /xmlrpc.php)' %s > %s" % (self.wp_log, self.xmlrpc_log)
        dmp_tables = "iptables -F"
        # Gross hack - figure out python - iptables interaction
        # Dump all the tables
        self.shell_cmd(dmp_tables)
        # Run a grep for any xmlrpc posts
        self.shell_cmd(grp_cmd)
        # Parsing out the ips
        ips = self.grab_ips()
        # Loop around the ips and do the needful
        for ip in ips:
            ip_tbls = "iptables -I INPUT -s %s -j DROP" % ip
            print "[*] Banning %s " % str(ip)
            self.write_ban_log("%s => Banned IP: %s \n" % (self.timestamp, ip))
            self.shell_cmd(ip_tbls)


if __name__ == '__main__':
    try:
        if os.getuid() != 0:
            print "[!!] Please run as root."
            sys.exit(1)
        else:
            block = Block_Xmlrpc()
            block.main()
    except Exception, err:
        print "[-] Error: %s " % err
