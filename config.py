import ConfigParser

MODE_BUTTON = 0x30
MODE_BUTTON_ACCELEROMETER = 0x31

SLEEP_DURATION = 5
SOCK_TIMEOUT_DURATION = 0.1

DEBUG = True

DISCOVER_DURATION = 5

# Buttons parameters
BUTTON_ACTION = {
    "left": "/usr/bin/xmms --rew",
    "right": "/usr/bin/xmms --fwd",
    "up": "",
    "down": "",
    "plus": "amixer set PCM 2dB+",
    "minus": "amixer set PCM 2dB-",
    "A": "/usr/bin/xmms --play-pause",
    "B": "sudo acpitool -s",
    }

# Those buttons are used by default by the application
# BUTTON_HOME = ""
# BUTTON_1 = ""
# BUTTON_2 = ""

# Accelerometer parameters
ACCELEROMETER_ZERO = 0x80
ACCELEROMETER_PRECISION = 0x20

ACCEL_X_LEFT_ACTION  = "/usr/bin/xmms --rew"
ACCEL_X_RIGHT_ACTION = "/usr/bin/xmms --fwd"
ACCEL_Y_UP_ACTION    = "echo VERT_UP > /dev/null"
ACCEL_Y_DOWN_ACTION  = "echo VERT_DOWN > /dev/null"
ACCEL_Z_FRONT_ACTION = "echo DEPTH_FRONT > /dev/null"
ACCEL_Z_BACK_ACTION  = "echo DEPTH_BACK > /dev/null"


def readConfig(file="config.ini"):
    Config = ConfigParser.ConfigParser()
    Config.read(file)
    sections = Config.sections()

                                        
