import time


def switchRumble(wiimote):
    """
    Switch the rumble
    """
    rumble_flag = 1 << 0
    
    if wiimote.feature & rumble_flag :
        wiimote.feature &= ~rumble_flag
    else:
        wiimote.feature |= rumble_flag
        
    wiimote.change_feature(wiimote.feature)


def setTimeRumble(wiimote, dur):
    """
    Activate the rumbe for dur seconds then
    shut it down.
    """
    switchRumble(wiimote)
    time.sleep(dur)
    switchRumble(wiimote)

