class HitTokenError(Exception):
    def __init__(self, msg):
        Exception.__init__(self, msg)


class ParamsError(Exception):
    def __init__(self, msg):
        Exception.__init__(self, msg)


class GetTokenError(Exception):
    def __init__(self):
        Exception.__init__(self)
