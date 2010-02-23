import logging
from moduleskel import Module

class Speaker (Module) :
    """
    Speaker implementation
    """

    ENABLE  = 0x01
    MUTE    = 0x02

    MAX_SIZE = 0x14
    
    def __init__(self, wiimote):
        """
        Initialisation sequence is described at
        http://wiibrew.org/wiki/Wiimote#Initialization_Sequence
        """
        Module.__init__(self, wiimote)
        self.flags = 0

        # start 7-step initialisation sequence
        # 1. Enable speaker
        # 2. Mute speaker
        # 3. Write 0x01 to register 0xa20009
        # 4. Write 0x08 to register 0xa20001
        # 5. Write 7-byte configuration to registers 0xa20001-0xa20008
        # 6. Write 0x01 to register 0xa20008
        # 7. Unmute speaker (so we can hear, dah)
        
        self.enableSpeaker() # 1
        self.muteSpeaker() # 2
        
        self.wiimote.write_registers([0xa2, 0x00, 0x09], [0x01]) # 3
        if wiimote.logger.isEnabledFor(logging.DEBUG):
            wiimote.logger.debug("Write registers 1 : ok ")

        self.wiimote.write_registers([0xa2, 0x00, 0x01], [0x08]) # 4
        if wiimote.logger.isEnabledFor(logging.DEBUG):
            wiimote.logger.debug("Write registers 2 : ok ")

        self.setSpeakerConfiguration() # 5
        if wiimote.logger.isEnabledFor(logging.DEBUG):
            wiimote.logger.debug("Configuration : ok ")
        
        self.wiimote.write_registers([0xa2, 0x00, 0x08], [0x01]) # 6
        if wiimote.logger.isEnabledFor(logging.DEBUG):
            wiimote.logger.debug("Write registers 3 : ok ")

        self.unmuteSpeaker()  # 7

        if wiimote.logger.isEnabledFor(logging.INFO):
            wiimote.logger.info ("Speaker initialisation done")

        # init is done, let's play :)
        # self.play([0x00, 0x00]) # <- get input somewhere
        with open("/home/chris/code/pywii/misc/prepare.wav", "r") as wav :
            data = wav.read(self.MAX_SIZE)
            while data != '':
                self.play(data)
                data = wav.read(self.MAX_SIZE)
                
        
    def shutup(self):
        """
        Shuts down the speaker. Note that as long the speaker won't have to be
        reinitialized, if re-enabled
        """
        self.muteSpeaker()
        self.disableSpeaker()
        

    def switchSpeaker(self, action):
        """
        Switch speaker activation flag depending on action type.
        Action can be ENABLE or MUTE (otherwise exception raised)
        1. Check action type and get matching code
        2. Switch flag and get writing code (or not)
        3. Send report to Wiimote
        """
        
        if not (action & self.ENABLE) or not (action & self.MUTE) :
            raise NotImplementedError("This action does not exist")
        
        if action & self.ENABLE :
            action_byte = chr(0x14) 
        elif action & self.MUTE :
            action_byte = chr(0x19)
                
        if self.flags & action :
            self.flags &= ~action
            value_byte = chr(0x00)
        else :
            self.flags |= action
            value_byte = chr(0x04)

        self.wiimote.send_control_frame( [action_byte, value_byte] )

        
    # Following 4 functions are just to simplify understanding
    # "Readability counts."
    def enableSpeaker(self):
        if not (self.flags & self.ENABLE):
            self.switchSpeaker(self.ENABLE)

            
    def disableSpeaker(self):
        if self.flags & self.ENABLE:
            self.switchSpeaker(self.ENABLE)

            
    def muteSpeaker(self):
        if not (self.flags & self.MUTE):
            self.switchSpeaker(self.MUTE)

            
    def unmuteSpeaker(self):
        if self.flags & self.MUTE:
            self.switchSpeaker(self.MUTE)            

            
    def setSpeakerConfiguration(self):
        offset = [0xa2, 0x00, 0x01]
        # 4-bit AD PCM sound at 3000Hz
        # sample_pcm = "00 00 D0 07 40 00 00"
        # 8-bit PCM sound at 1500Hz sample rate
        sample_pcm = [0x00, 0x40, 0x40, 0x1f, 0x40, 0x00, 0x00]
        
        self.wiimote.write_registers(offset, sample_pcm) 

        
    def play(self,bytes):
        bytes  = [x for x in bytes] 
        length = len(bytes)
        
        if not (0 < length <= self.MAX_SIZE ): return

        frame = [chr(0x18), chr(length)]
        frame.extend(bytes)
        self.wiimote.send_control_frame(frame)
