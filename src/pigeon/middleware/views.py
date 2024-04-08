import pigeon.default.errors as default_error
from pigeon.middleware.conversion.converter import autogenerator
from pigeon.conf import Manager
from pigeon.http import HTTPResponse, HTTPRequest
from typing import Callable
from collections import UserDict
from pigeon.utils.common import ParameterDict
import re


class View:
    def __init__(self, target: str, func: Callable, mimetype: str, auth: str):
        self.target = target
        self.func = lambda request, dynamic_params=None: func(request, dynamic_params) if dynamic_params else func(request)
        self.mimetype = mimetype
        self.auth = auth
        
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

    def register(self, target, func, mimetype, auth):
        """
        Add new view to ViewHandler instance.
        """
        self.views.append(View(target, func, mimetype, auth))

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

    def get_auth(self, target, mimetype):
        """
        Returns the auth required for the view at <target>
        """
        view = self._get_view(target, mimetype)
        # non-existing view cannot have auth
        if not view:
            return None
        return view.auth

    def get_func(self, path: str, mimetype: str) -> Callable | None:
        """
        Returns a decorated version (includes dynamic_params and auth) of the view for the requested path.
        """
        view = self._get_view(path, mimetype)
        if not view:
            # no view found
            return None
        dynamic_params = view.get_dynamic(path)

        def wrapper(request):
            # wrap in autogenerator for automatic type conversion
            wrapped_view: View = autogenerator(view)
            # warp in auth for auth features
            wrapped_view: View = Manager.auth_handler.wrap(wrapped_view)
            return wrapped_view(request, dynamic_params)
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
