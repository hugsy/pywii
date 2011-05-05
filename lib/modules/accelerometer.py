from logging import DEBUG
from subprocess import Popen
from moduleskel import Module


class Accelerometer (Module):
    """
    This class handles all accelerometer movement. It is a bit fuzzy,
    but is really coherent after a short moment.
    Please see http://wiibrew.org/wiki/Wiimote#Accelerometer for more
    details
    """

    def __init__(self, wiimote):
        """ Starts the module """
        Module.__init__(self, wiimote)
        
        
    def update(self,bytes):
        """ Extract positions from frame. """
        x,y,z = bytes[0:3]

        self.update_horizon(x)
        self.update_vertical(y)
        self.update_depth(z)


    def perform_action(self,move):
        """ Execute system call corresponding to movement """
        if move not in ('up','down','left','right','back','front'):
            self.wiimote.logger.error("Unknown movement %s" % move)
            return
    
        if self.wiimote.logger.isEnabledFor(DEBUG) :
            self.wiimote.logger.debug("%s movement detected" % move)
        
        cmd = self.wiimote.cfg.ACCEL_ACTION[move]
        self.wiimote.logger.info ("System command : %s" % cmd)
        Popen([cmd], shell=True)
     
    
    def update_horizon(self,x_pos):
        """ Detecting horizontal movement """
        if x_pos < self.wiimote.cfg.ACCELEROMETER_ZERO - self.wiimote.cfg.ACCELEROMETER_PRECISION :
            self.perform_action("left")
        
        if x_pos > self.wiimote.cfg.ACCELEROMETER_ZERO + self.wiimote.cfg.ACCELEROMETER_PRECISION :
            self.perform_action("right")

        
    def update_vertical(self,y_pos):
        """ Detecting depth movement """
        if y_pos > self.wiimote.cfg.ACCELEROMETER_ZERO + self.wiimote.cfg.ACCELEROMETER_PRECISION :
            self.perform_action("back")
        
        if y_pos < self.wiimote.cfg.ACCELEROMETER_ZERO - self.wiimote.cfg.ACCELEROMETER_PRECISION :
            self.perform_action("front")

            
    def update_depth(self,z_pos):
        """ Detecting vertical movement """
        if z_pos < self.wiimote.cfg.ACCELEROMETER_ZERO - self.wiimote.cfg.ACCELEROMETER_PRECISION :
            self.perform_action("up")
        
        if z_pos > self.wiimote.cfg.ACCELEROMETER_ZERO + self.wiimote.cfg.ACCELEROMETER_PRECISION :
            self.perform_action("down")
