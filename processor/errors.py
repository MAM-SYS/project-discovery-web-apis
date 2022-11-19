SubfinderBaseCode = 1000
NucleiBaseCode = 2000


class SubfinderException(Exception):
    code = SubfinderBaseCode

    def __init__(self, message: str):
        self.message = message
        self.code = self.code
