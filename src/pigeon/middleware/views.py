from typing import Callable
from collections import UserDict


class ParameterDict(UserDict):
    def __getattr__(self, key):
        return self.data.get(key)


class View:
    def __init__(self, target: str, func: Callable, mimetype: str):
        self.target = target
        self.func = func
        self.mimetype = mimetype
        
    def match(self, path: str) -> bool:
        ...
    
    def get_dynamic(self, path: str) -> ParameterDict:
        """
        Returns dict of dynamic params
        """
        ...
    
    
class ViewHandler:
    def __init__(self):
        self.views = ...
        ...


class Error:
    def __init__(self, status):
        self.status = status
    
    
class ErrorHandler:
    def __init__(self):
        self.errors = ...
