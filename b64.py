#!/usr/bin/env python
#
# Little script with some logic
# to base64 encode and decode depending
# on users input.
#========================================

import sys


def decodeb64(info):
    """This function will decode a base64 string
    """
    decode = raw_input("Enter base64 string to decode: \n> ")
    result = decode.decode('base64')
    print "\033[32m[-]\033[0m Decoded base64: "
    print result

def encodeb64(info):
    """This function will encode a string in base64
    """
    encode = raw_input("Enter base64 string to encode: \n> ")
    result = encode.encode('base64')
    print "\033[34m[-]\033[0m Encoded base64: "
    print result

if __name__ == '__main__':
    info = raw_input("Decode or Encode? ").lower()
    try:
        if "decode" in info:
            decodeb64(info)
        elif "encode" in info:
            encodeb64(info)
        else:
            sys.exit("\033[31m[!]\033[0m That input was not relevant!")
    except Exception, err:
        print "\033[31m[!]\033[0m Error %s" % err
