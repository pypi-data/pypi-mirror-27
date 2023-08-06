

class ZapFormatException(Exception):

    def __init__(self, message: str = ""):
        Exception.__init__(self, message)


class ZapBotCommandRunException(Exception):

    def __init__(self, message: str = ""):
        Exception.__init__(self, message)
