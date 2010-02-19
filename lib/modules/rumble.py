import time

class Rumble :
    """
    
    This module handles the rumble on the Wiimote
    
    """

    def __init__(self, wiimote):
        self.wiimote = wiimote

        
    def switchRumble(self):
        """
        Switch the rumble.
        """
        rumble_flag = 1 << 0
    
        if self.wiimote.feature & rumble_flag :
            self.wiimote.feature &= ~rumble_flag
        else:
            self.wiimote.feature |= rumble_flag
        
        self.wiimote.change_feature(self.wiimote.feature)

        
    def setTimeRumble(self, dur):
        """
        Activate the rumbe for dur seconds then shut it down.
        """
        self.switchRumble()
        time.sleep(dur)
        self.switchRumble()

