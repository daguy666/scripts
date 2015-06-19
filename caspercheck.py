#!/usr/bin/env python
#First crack at jamf detection.
#There are a few ways to detect if a system has jamf running.
#I will try and detect them.
#|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||

import sys
import os
import socket
import getpass
import commands
import platform
import datetime
import subprocess

def jamf_connect():
    jss_avail = subprocess.call(["jamf", "checkJSSConnection", "-retry", "1"])
    if jss_avail == 0:
        return True
    else:
        return False

def jamf_process():
    """This function will check the jamf process
        and make sure its running.
    """
    jamf_proc = commands.getoutput('ps -A')
    if 'jamf' in jamf_proc:
        return True
    else:
        return False


def system_info():
    """This function will gather data about
        the system user and network info.
    """
    system = {}
    host = socket.gethostname()
    username = getpass.getuser()
    ip   = socket.gethostbyname(socket.gethostname())
    os_ver = platform.mac_ver()[0]
    system['host'] = host
    system['username'] = username
    system['ip'] = ip
    system['os'] = os_ver
    return system

def fileCheck(file_name):
    """checks that the jamf file is installed
        on the machine.
    """
    if os.path.isfile(file_name):
        return True
    else:
        return False

time = datetime.datetime.now()

try:
    info = system_info()
    proc = jamf_process()

    jamf_file = fileCheck("/usr/sbin/jamf")
    jamfAgents = fileCheck("/usr/sbin/jamfAgent")

    if proc == True:
        print("ok its cool")
    else:
        sys_info = system_info()

        log_file = open("caspercheck.log", 'a+')
        log_file.write(str(time) + " " + str(sys_info) + "\n")
        log_file.close()

except Exception, err:
    print "[!] Error: %s" % err
