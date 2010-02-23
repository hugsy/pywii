from time import sleep
from moduleskel import Module 

class Rumble (Module) :
    """
    
    This module handles the rumble on the Wiimote
    
    """

    def __init__(self, wiimote):
        Module.__init__(self,wiimote)

        
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
        sleep(dur)
        self.switchRumble()

