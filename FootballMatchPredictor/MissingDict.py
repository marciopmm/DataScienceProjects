class MissingDict(dict):
    __missing__ = lambda self, key: key