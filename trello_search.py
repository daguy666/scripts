#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------
# Filename      : trello_search.py
# Description   :
# Created By    : Joe Pistone
# Date Created  : 16-Mar-2017 10:07
# Date Modified :
#
# License       : Development
#
# Description   : Search for trello users
#
# (c) Copyright 2017, TheKillingTime all rights reserved.
#-----------------------------------------------------------

__author__  = "Joe Pistone"
__version__ = "0.1"

import sys
import json
import urllib2

class Search_Trello(object):

    def __init__(self, search_term):
        self.terms = search_term
        self.trello_url = "https://api.trello.com/1/search/members?query=%s" % self.terms

    def make_call(self):
        """
        Calls the Trello Api.
        """
        try:
            request = urllib2.Request(self.trello_url)
            self.result = urllib2.urlopen(request)
        except urllib2.HTTPError, e:
            
            if e.code == 400:
                print "[!] Bad Request"
            elif e.code == 404:
                print "[!] Page Not found."
            else:
                print "[!] Error calling Api %s " % e
    
    def parse_output(self):
        """
        Parses the output of the result.
        """
        try:
            trello_output = json.load(self.result)
            for name in trello_output:
                print "-" * 25 
                print "[+] Full Name: %s " % name['fullName']
                print "[+] Username: %s " % name['username']
                print "[+] Initials: %s " % name['initials']              
        except UnicodeEncodeError:
            print "[!] UnicodeEncodeError."

    def main(self):
        """
        Start it up.
        """
        self.make_call()
        self.parse_output()
        print "-" * 25
      

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print "[!] Usage %s <who to search for>"
        sys.exit(1)
   
    search_term = sys.argv[1]
    if search_term.isalnum():
        st = Search_Trello(search_term)
        st.main()
    else:
        print "[!] Alpha numeric searches please."
