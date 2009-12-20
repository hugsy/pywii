#!/usr/bin/env python
# $ File: /home/chris/code/pywii/main.py $
# $ MD5: 7fc0955fb4163304155c0c3ccb12908c $
# $ By Chris A <tuxxychris[at]gmail[dot]com> $ 
# $ Last-Modified: Sun Dec 13 16:50:26 2009 $ 

__author__  = "hugsy"
__version__ = 0.2
__licence__ = "WTFPL v.2"
__file__    = "/home/chris/code/pywii/pywii.py"
__doc__     = """ 

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

All suggestions welcomed at tuxxychris at gmail dot com 

""" 

from config import SLEEP_DURATION
from lib.wiimote import Wiimote
from lib.base import find_wiimotes
from time import sleep

if __name__ == "__main__":
    # wiimotes = [('00:19:1D:B7:43:0D', 'Nintendo RVL-CNT-01')] # for debug 
    wiimotes = []
    attempts = 5
    wiimote_threads = []
    
    while attempts :
        wiimotes = find_wiimotes()
        attempts -= 1
        if len(wiimotes) :
            break
        else :
            sleep (SLEEP_DURATION)

    if len(wiimotes) == 0 :
        print ("No Wiimote found")
        exit (128)
    elif len(wiimotes) > 4 :
        print ("Cannot handle more than 4 Wiimotes for the moment")
        wiimotes = wiimotes[0:4]

    idx = 1
    for wm in wiimotes:
        wiimote = Wiimote(str(wm[0]), str(wm[1]), idx)
        wiimote.start()
        wiimote_threads.append(wiimote)
        idx += 1
        
    for wm in wiimote_threads :
        wm.join()
    
    exit (0)
