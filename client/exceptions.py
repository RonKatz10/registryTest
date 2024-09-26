class IPMissingError(Exception):
    def __init__(self, *args):
        super().__init__(*args)

class InvalidRegistry(Exception):
    def __init__(self, *args):
        super().__init__(*args)