#!/usr/bin/env python
""" 

Simple tool to make a bit of fun with your wiimote.
Can be used to interact with your system !

""" 

__author__="hugsy"
__version__=0.1
__licence__="WTFPL v.2"
__file__="/home/chris/code/pywii/pywii.py"

from config import DEBUG
from lib.wiimote import Wiimote
from lib.base import find_wiimotes

if __name__ == "__main__":
    if DEBUG :
        wiimote_addrs = [('00:19:1D:B7:43:0D', 'Nintendo RVL-CNT-01')]        
    else :
        wiimote_addrs = find_wiimotes()

    if len(wiimote_addrs) == 0 :
        print "No Wiimote found"
        exit (129)
        
    wii_num = 1
    wiimote_threads = []
    
    for wm in wiimote_addrs:
        if DEBUG: print "Creating Wiimote-%d" % wii_num
        wiimote = Wiimote(str(wm[0]), str(wm[1]), wii_num)
        wiimote.start()
        wiimote_threads.append(wiimote)
        
        wii_num += 1
        if wii_num > 4 :
            print "Cannot handle more than 4 Wiimotes"
            exit (130)

    if wii_num > 1:
        for wm in wiimote_threads :
            wm.join()
    
    exit (0)
