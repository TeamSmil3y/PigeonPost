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
        super().__init__()
        if data: self.data.update(data)
    
    def __getattr__(self, key):
        return self.data.get(key)
