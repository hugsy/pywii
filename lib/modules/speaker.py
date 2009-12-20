class Speaker :
    """
    Speaker implementation
    """

    ENABLE  = 0x01
    MUTE    = 0x02
    
    def __init__(self, wiimote):
        """
        Initialisation sequence is described at http://wiibrew.org/wiki/Wiimote#Initialization_Sequence
        """
        self.wiimote = wiimote
        self.flags = 0

        # start 7-step initialisation sequence
        self.enableSpeaker() # Enable speaker
        self.muteSpeaker() # Mute speaker
        self.wiimote.write_registers([0xa2, 0x00, 0x09], [0x01]) # Write 0x01 to register 0xa20009
        self.wiimote.write_registers([0xa2, 0x00, 0x01], [0x08]) # Write 0x08 to register 0xa20001
        self.setSpeakerConfiguration() # Write 7-byte configuration to registers 0xa20001-0xa20008
        self.wiimote.write_registers([0xa2, 0x00, 0x08], [0x01]) # Write 0x01 to register 0xa20008
        self.unmuteSpeaker()  # Unmute speaker (so we can hear)

        # init is done, let's play :)
        self.play([0x00, 0x00]) # <- get input somewhere

        # shutting down
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
        if action & self.ENABLE or action & self.MUTE :
            if action & self.ENABLE :
                action_byte = chr(0x14) 
            else :
                action_byte = chr(0x19)
                
            if self.flags & action :
                self.flags &= ~action
                value_byte = chr(0x00)
            else :
                self.flags |= action
                value_byte = chr(0x04)

        else :
            raise NotImplementedError("This action does not exist")
        
        self.wiimote.send_control_frame( [action_byte, value_byte] )

    # Following 4 functions are just to simplify understanding
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

    def play(bytes):
        length = len(bytes)
        
        if not (1 <= length <= 20) :
            return

        self.wiimote.send_control_frame([0x18, length, bytes])
