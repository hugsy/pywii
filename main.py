#!/usr/bin/env python
# $ File: /home/chris/code/pywii/main.py $
# $ MD5: c6cda562a1a794bf15f4df08ea1f8aae $
# $ By Chris A <tuxxychris[at]gmail[dot]com> $ 
# $ Last-Modified: Sun Dec 20 13:16:18 2009 $ 

__author__  = "hugsy"
__version__ = 0.1
__licence__ = "GPL v.2"
__file__    = "pywii.py"
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

The only pre-requisite for PyWii to work is the PyBluez library, available at
https://code.google.com/pybluez.

Enjoy 
""" 

from server import Server, Daemon
from config import daemon


if __name__ == "__main__":

    
    if DAEMONIZE :
        Daemon(Server())
    else :
        Server()
        
    exit (0)
