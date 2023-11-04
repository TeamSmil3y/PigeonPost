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
        """
        Check for the requested path matching the views target.
        """

        target = re.sub(r"\{\{(.*?)\}\}", r"[^/]{1,}", self.target)
        pattern = re.compile(target)
        return bool(pattern.match(path))
    
    def get_dynamic(self, path: str) -> ParameterDict:
        """
        Returns dict of dynamic url params.
        """

        target = self.target

        names_list = re.findall(r"\{\{[^\}]{1,}\}\}", target)

        target_ = target
        for name in names_list:
            target_ = target_.replace(name, "\sep")

        sep = {i for i in target_.split("\sep") if i != ""}

        for s in sep:
            target = target.replace(s, "/")
            path = path.replace(s, "/")

        names = {}
        params = ParameterDict()

        for n, i in enumerate(target.split("/")):
            if i.startswith("{{") and i.endswith("}}"):
                names[n] = i.replace("{{", "").replace("}}", "")

        for n, i in enumerate(path.split("/")):
            if n in names:
                params[names[n]] = i

        return params  


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
