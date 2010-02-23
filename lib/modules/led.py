from time import sleep
from moduleskel import Module


class Led (Module):
    """
    This class handles the LED module.
    """

    def __init__(self,wiimote):
        Module.__init__(self,wiimote)

    
    def switchLed(self, diod):
        """
        Switch led status (if on -> off and reverse :))
        """
    
        # led_flag = 1 << ( 5 - diod )
        led_flag = 1 << ( diod + 3 )
    
        if self.wiimote.feature & led_flag :
            self.wiimote.feature &= ~led_flag
        else:
            self.wiimote.feature |= led_flag
            
        self.wiimote.change_feature(self.wiimote.feature)

    
    def blink(self, length, repeat, diod):
        """
        Make the wiimote led pointed by `diod` to blink
        The wiimote will blink (repeat x 2) times with a gap
        of length seconds
        """
        for i in range(repeat * 2):
            self.switchLed(diod)
            sleep (length)
        
