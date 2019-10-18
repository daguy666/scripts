#!/usr/bin/env python
# The idea behind this was one was simple 
# I dont like reading xml, personally I find json easier to read.
# ----------------------------------------------------------------
#
# You can also add this to your bashrc or bash_profile as an alias,
# then you can run it anywhere! 
# -----------------------------------------------------------------

try:
    import os
    import sys
    import biplist

    from pprint import pprint

except ImportError, err: 
    print "[!] Import Error: %s " % err
    sys.exit(1)

def read_binary_plist(bplist):
    try:
        if os.path.exists(bplist):
            pprint(biplist.readPlist(bplist))
        else:
            print "[!] Path does not exist."
    except biplist.InvalidPlistException:
        print "[!] Unable to open file."

if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit('[!] Usage %s </path/to/plist>' % sys.argv[0])

    # set the first cmd arg to the path of the plist
    bplist = sys.argv[1]
    read_binary_plist(bplist)
