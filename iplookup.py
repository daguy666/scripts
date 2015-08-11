#!/usr/bin/env python
#\\\\\\\\\\\\\\\\\\\\\\\\\\
#=======================\\\
# TODO
''' Finish this script. Goal is to do something like 
    a netstat for tcp and check all established connecttions. 
    This is not functioning yet. Still needs a bunch of work.  
    netstat | grep -i established | awk '{print $5}' 
'''


 
import subprocess
from ipwhois import IPWhois

def getIpList():
    '''Opens a file with ip addresses in
       list format.
    '''
    f = open('ipList.txt')
    ipList = f.read()
    return ipList
    

def whoIs(ipList):
    '''This will run the command to search
       who is and gather information on the 
       ip addresses.
    '''
    for ip in ipList:
        cmd = '/usr/bin/whois %s | grep -i "domain name:" | grep -i "country"' % ip
        cmdEx = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        output = cmdEx.communicate()[0]
        return output

def ipLookUp(ipList):
    # Example
    # IPWhois(ip).lookup_rws()
    info = []
    lookup = IPWhois(ip).lookup_rws() 
    for ip in ipList:
        print ip
        


if __name__ == '__main__':
    print whoIs(getIpList())
