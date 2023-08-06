class CacheTokenError(Exception):
    def __init__(self):
        Exception.__init__(self, 'cache token error')


class ParameterError(Exception):
    def __init__(self):
        Exception.__init__(self, 'parameter error')