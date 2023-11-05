import pigeon.default.errors as default_error
from pigeon.http import HTTPResponse, HTTPRequest
from typing import Callable
from collections import UserDict
import re


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

        target = re.sub(r"{{(.*?)}}", r"[^/]{1,}", self.target)+'(\\?.*)?$'

        pattern = re.compile(target)
        return bool(pattern.match(path))
    
    def __call__(self, request, dynamic_params=None):
        if dynamic_params:
            return self.func(request, dynamic_params)
        else:
            return self.func(request)

    def get_dynamic(self, path: str) -> ParameterDict:
        """
        Returns dict of dynamic url params.
        """

        target = self.target

        names_list = re.findall(r"\{\{[^\}]{1,}\}\}", target)

        target_ = target

        for name in names_list:
            # add seperator to identify regions between the params
            target_ = target_.replace(name, "\sep")

        # generate a set of all of the ..?s
        sep = {i for i in target_.split("\sep") if i}

        for s in sep:
            # replace the regions betweeen the params with /
            target = target.replace(s, "/")
            # replace the regions betweeen the params with /
            path = path.replace(s, "/")

        names = {}
        params = ParameterDict()

        # iterate over the params where n is the param-name index and i is the param
        for n, i in enumerate(target.split("/")):
            if i.startswith("{{") and i.endswith("}}"):
                # build names dictionary where the index n is the key and the param-name the value
                names[n] = i.replace("{{", "").replace("}}", "")

        # iterate over the params where n is the params index and i is the param
        for n, i in enumerate(path.split("/")):
            # check if the param really is a param
            if n in names:
                # build ParameterDict where the key is the param-name and the value is the actual param
                params[names[n]] = i

        return params  


class ViewHandler:
    def __init__(self):
        self.views: list[View] = []

    def register(self, target, func, mimetype):
        """
        Add new view to ViewHandler instance.
        """
        self.views.append(View(target, func, mimetype))

    def _get_view(self, path: str, mimetype: str) -> View | None:
        """
        returns view object matching path and mimetype.
        """
        for view in self.views:
            if view.match(path):
                if view.mimetype == mimetype:
                    return view
        # no view found
        return None

    def get_func(self, path: str, mimetype: str) -> Callable | None:
        """
        Returns a decorated version (includes dynamic_params) of the view for the requested path.
        """
        view = self._get_view(path, mimetype)
        if not view:
            # no view found
            return None
        dynamic_params = view.get_dynamic(path)

        def wrapper(request):
            return view(request, dynamic_params)
        return wrapper

    def get_available_mimetypes(self, path: str) -> list[str]:
        """
        Returns a list of available mimetypes for the requested path.
        """
        available_mimetypes = []
        for view in self.views:
            if view.match(path):
                available_mimetypes.append(view.mimetype)
        available_mimetypes.sort(key=lambda value: value.count('*'))
        return available_mimetypes


class ErrorHandler:
    def __init__(self):
        """
        On initilization autoregister default fallback error func
        """
        self.errors = {
            0: default_error.fallback,
        }

    def register(self, code: int, func: Callable):
        """
        Add new error to ErrorHandler instance.
        """
        self.errors[code] = func

    def get_func(self, code: int) -> Callable:
        """
        Get error func for code or fallback if no func known for specified code
        """

        return self.errors.get(code) or (lambda request=None: self.errors[0](request, code))

    def __call__(self, code: int, request: HTTPRequest = None) -> HTTPResponse | str:
        """
        call error code matching func (fallback if no func for the specified code exists)
        request parameter optional
        """

        if HTTPRequest:
            return self.get_func(code)(request=request)

        return self.get_func(code)()
