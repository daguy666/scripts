#!/usr/bin/env python
#is there a kcpassword file?

import os
import getpass
import datetime
import platform

def fileCheck(file_name):
    """This function will locate a file 
       Then return true or false depending on existance
    """
    if os.path.isfile(file_name):
        return True
    else:
        return False

def systemInfo():
    """This function gets the username and os_version
    """
    system = {}
    username = getpass.getuser()
    os_ver = platform.mac_ver()[0]
    system['username'] = username
    system['os_ver'] = os_ver
    return system
    
if __name__ == "__main__":
    fileexists = fileCheck("/etc/kcpassword")
    time = datetime.datetime.now()
    try:
        if fileexists:
            log = systemInfo()
            log_file = open("kc.log","a+")
            log_file.write(str(time) + " KCPassword Detected! " + str(log) + "\n")
            log_file.close
        else:
            print "No KCPassword file found."
    except Exception, err:
        print "[!] Error: %s" % err 
