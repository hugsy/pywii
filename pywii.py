#!/usr/bin/env python
# -*- coding : utf-8 -*-
# -*- mode: python -*-

""" 
Simple tool to make a bit of fun with your wiimote.
Can be used to interact with your system !

""" 

__author__="hugsy"
__version__=0.1
__licence__="WTFPL v.2"
__doc__="Yet another stupid tool"
__file__="/home/chris/Documents/projets/pywii/pywii.py"

from config import DEBUG
from wiimote import Wiimote, find_wiimotes 

if __name__ == "__main__":
    # wiimote_addrs = find_wiimotes()
    wiimote_addrs = [('00:19:1D:B7:43:0D', 'Nintendo RVL-CNT-01')]

    if wiimote_addrs is None :
        print "Fail to access bluetooth device"
        exit (128)
    elif len(wiimote_addrs) == 0 :
        print "No Wiimote found"
        exit (129)
        
    wii_num = 1
    wiimotes = []
    
    for wm in wiimote_addrs:
        if DEBUG: print "Creating Wiimote-%d" % wii_num
        wiimotes.append( Wiimote(str(wm[0]), str(wm[1]), wii_num).start() )
        
        wii_num += 1
        if wii_num > 4 :
            print "Cannot handle more than 4 Wiimotes"
            exit (130)

    for wiimote in wiimotes :
        if wiimote is not None :
            wiimote.join()
    
    exit (0)
