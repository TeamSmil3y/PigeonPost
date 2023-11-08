"""
List of classes that represent rather abstract data types
"""

from collections import UserDict


class ParameterDict(UserDict):
    """
    Similar to a dictionary, but items can also be accessed using <dict>.<key>.
    If accessed as described above, the dict will return the value or None if no matching item is found.
    """
    def __init__(self, data: dict=None):
        super().__init__(data)

    def keys(self):
        return self.data.keys()

    def items(self):
        return self.data.items()

    def values(self):
        return self.data.values()

    def __getattr__(self, key):
        return self.data.get(key)

class LowerParameterDict(ParameterDict):
    """
    Similar to ParameterDict, but all keys will be changed to lowercase and any dashes '-' in keys will be changed to underscores '_'.
    """
    def __init__(self, data: dict=None):
        data = {LowerParameterDict._lower_key(key): value for key, value in data.items()}
        super().__init__(data)

    @classmethod
    def _lower_key(cls, key):
        return key.replace('-', '_').lower()

    def __getattr__(self, key):
        return self.data.get(LowerParameterDict._lower_key(key))