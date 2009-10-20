#!/usr/bin/env python

__author__ = "hugsy"
__version__ = 0.2
__licence__ = "WTFPL v.2"
__file__ = "/home/chris/code/pywii/pywii.py"
__doc__ = """ 

This simple tool was basically written because I'm lazy,
and is purposed to make a bit of fun with your wiimote
allowing to interact (simply) with your system. Some events
(buttons pressing, wiimote moves) can be match to perform a
specific action on your system.

Up to 4 Wiimotes can be used simultaneously (but I don't see
the point in that :) ).

Features provided :
- full button handling (native since v0.1)
- led handler
- rumble handler
- accelerometer handler

Yet-to-come features :
- speaker (I'm actually working on it right now)
- camera 

All suggestions welcomed.

""" 

from config import DEBUG
from lib.wiimote import Wiimote
from lib.base import find_wiimotes

if __name__ == "__main__":
    if DEBUG :
        wiimote_addrs = [('00:19:1D:B7:43:0D', 'Nintendo RVL-CNT-01')]
    else :
        wiimote_addrs = find_wiimotes()

    if len(wiimote_addrs) == 0 :
        print ("No Wiimote found")
        exit (129)

    elif len(wiimote_addrs) > 4 :
        print "Cannot handle more than 4 Wiimotes for the moment"
        exit (130)
        
    wii_num = 1
    wiimote_threads = []
    
    for wm in wiimote_addrs:
        print ("Creating Wiimote-%d" % wii_num)
        wiimote = Wiimote(str(wm[0]), str(wm[1]), wii_num)
        wiimote.start()
        wiimote_threads.append(wiimote)
        
        wii_num += 1

        if wii_num > 4 :
            print ("Cannot handle more than 4 Wiimotes")
            exit (130)

    for wm in wiimote_threads : wm.join()
    
    exit (0)
