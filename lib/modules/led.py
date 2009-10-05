import time


def switchLed(wiimote):
    """
    Switch led status
    """
    led_flag = 1 << ( 5 - wiimote.number )
    
    if wiimote.feature & led_flag :
        wiimote.feature &= ~led_flag
    else:
        wiimote.feature |= led_flag
        
    wiimote.change_feature(wiimote.feature)

    
def blink(wiimote, dur, repeat):
    """
    Make the wiimote led blinking.
    The wiimote will blink (repeat x 2) times with a gap
    of dur seconds
    """
    for i in range(repeat * 2 + 1):
        switchLed (wiimote)
        time.sleep(dur)
        
