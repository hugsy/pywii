from ConfigParser import ConfigParser

class PywiiConfig :
    """
    Configuration parser
    """
    
    def __init__(self, configfile):
        """ PyWiiconfig initialization """
        
        CFG = ConfigParser()
        CFG.read(configfile)
       
        # self.DEBUG                   = CFG.getboolean("main", "DEBUG")
        self.DEBUG_LEVEL             = CFG.getint("main", "DEBUG_LEVEL")
        self.SLEEP_DURATION          = CFG.getint("main", "SLEEP_DURATION")
        # self.DISCOVER_DURATION       = CFG.getint("main", "DISCOVER_DURATION")
        self.SOCK_TIMEOUT_DURATION   = CFG.getfloat("main", "SOCK_TIMEOUT_DURATION")
        # self.DAEMONIZE               = CFG.getboolean("main", "DAEMONIZE")

        self.ON_EXIT_HOOK             = CFG.get("main", "ON_EXIT_HOOK")
        
        # wiimote buttons map is at http://wiibrew.org/wiki/Wiimote#Core_Buttons
        # temp hacks
        BUTTON_HOME = "quit"
        BUTTON_1 = "accel"
        BUTTON_2 = "status"

        self.keymap = range(0,8)
        self.keymap[0] = [CFG.get("button_action", "BUTTON_ACTION_LEFT"),
                          BUTTON_2]
        self.keymap[1] = [CFG.get("button_action", "BUTTON_ACTION_RIGHT"),
                          BUTTON_1]
        self.keymap[2] = [CFG.get("button_action", "BUTTON_ACTION_DOWN"),
                          CFG.get("button_action", "BUTTON_ACTION_B")]
        self.keymap[3] = [CFG.get("button_action", "BUTTON_ACTION_UP"),
                          CFG.get("button_action", "BUTTON_ACTION_A")]
        self.keymap[4] = [CFG.get("button_action", "BUTTON_ACTION_PLUS"),
                          CFG.get("button_action", "BUTTON_ACTION_MINUS")]
        self.keymap[5] = [0, 0]
        self.keymap[6] = [0, 0]
        self.keymap[7] = [0, BUTTON_HOME]


        # accelerometer configuration
        self.ACCELEROMETER_ZERO       = CFG.getint("accel_config", "ACCELEROMETER_ZERO")
        self.ACCELEROMETER_PRECISION  = CFG.getint("accel_config", "ACCELEROMETER_PRECISION")

        self.ACCEL_ACTION = {
            "left"    : CFG.get("accel_action", "ACCEL_X_LEFT_ACTION"),
            "right"   : CFG.get("accel_action", "ACCEL_X_RIGHT_ACTION"),
            "up"      : CFG.get("accel_action", "ACCEL_Y_UP_ACTION"),
            "down"    : CFG.get("accel_action", "ACCEL_Y_DOWN_ACTION"),
            "front"   : CFG.get("accel_action", "ACCEL_Z_FRONT_ACTION"),
            "back"    : CFG.get("accel_action", "ACCEL_Z_BACK_ACTION"),
            }

