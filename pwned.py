#!/usr/bin/env python
#==============================================#
# This script checks emails addresses against  #
# the haveibeenpwned.com Api                   #
#==============================================#

__author__ = 'daguy666'

import json
import sys
import urllib2

email = sys.argv[1]
url   = 'https://haveibeenpwned.com/api/v2/breachedaccount/%s' % email
print "[-] Checking to see if your email is on any lists..."

try:
    request = urllib2.Request(url)
    result  = urllib2.urlopen(request)
except urllib2.HTTPError, e:

    if e.code == 404:
        sys.exit('[-] Your email address was not on any lists.')
    else:
        print "[!] Call to Api failed."

else:
    try:
        output = json.load(result)
    except Exception, err:
        print "[!] Error Deserializing Json. %s" % err
    print "[-] Your email was found on the following lists: "
    for entry in output:
        print "==> %s" %  entry['Name']
