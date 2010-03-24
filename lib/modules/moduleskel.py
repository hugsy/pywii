class Module:
    """
    Module generic class
    """
    def __init__(self, wiimote):
        self.wiimote = wiimote
        assert self.wiimote is not None
