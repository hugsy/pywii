"""

This module handles the LED mechanism.

"""
import time

def switchLed(wiimote, diod):
    """
    Switch led status
    """
    
    # led_flag = 1 << ( 5 - diod )
    led_flag = 1 << ( diod + 3 )
    
    if wiimote.feature & led_flag :
        wiimote.feature &= ~led_flag
    else:
        wiimote.feature |= led_flag
        
    wiimote.change_feature(wiimote.feature)

    
def blink(wiimote, length, repeat, diod):
    """
    Make the wiimote led pointed by `diod` to blink
    The wiimote will blink (repeat x 2) times with a gap
    of length seconds
    """
    for i in range(repeat * 2):
        switchLed (wiimote, diod)
        time.sleep (length)
        
