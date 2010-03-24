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
        
        
    def update(bytes):
        """ Extract positions from frame. """
        x,y,z = bytes[0:3]

        update_horizon(x)
        update_vertical(y)
        update_depth(z)


    def perform_action(move):
        """ Execute system call corresponding to movement """
        if move not in ('up','down','left','right','back','front'):
            self.wiimote.logger.error("Unknown movement %s" % move)
            return
    
        if self.wiimote.logger.isEnabledFor(logging.DEBUG) :
            self.wiimote.logger.debug("%s movement detected" % move)
        

        Popen([self.cfg.ACCEL_ACTION[move]], shell=True)
    
    
    def update_horizon(x_pos):
        """ Detecting horizontal movement """
        if x_pos < self.wiimote.cfg.ACCELEROMETER_ZERO - self.wiimote.cfg.ACCELEROMETER_PRECISION :
            perform_action('left')
        
        if x_pos > self.wiimote.cfg.ACCELEROMETER_ZERO + self.wiimote.cfg.ACCELEROMETER_PRECISION :
            perform_action('right')

        
    def update_vertical(y_pos):
        """ Detecting depth movement """
        if y_pos > self.wiimote.cfg.self.wiimote.cfg.ACCELEROMETER_ZERO + self.wiimote.cfg.self.wiimote.cfg.ACCELEROMETER_PRECISION :
            perform_action('front')
        
        if y_pos < self.wiimote.cfg.ACCELEROMETER_ZERO - self.wiimote.cfg.ACCELEROMETER_PRECISION :
            perform_action('back')

            
    def update_depth(z_pos):
        """ Detecting vertical movement """
        if z_pos < self.wiimote.cfg.ACCELEROMETER_ZERO - self.wiimote.cfg.ACCELEROMETER_PRECISION :
            perform_action('up')
        
        if z_pos > self.wiimote.cfg.ACCELEROMETER_ZERO + self.wiimote.cfg.ACCELEROMETER_PRECISION :
            perform_action('down')
