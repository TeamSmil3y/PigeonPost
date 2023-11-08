from pigeon.http import error, HTTPRequest, HTTPResponse
from typing import Any
import pigeon.utils.logger as logger
import base64

log = logger.Log('Auth', '#ff4a65')

class Credentials:
    def __init__(self, username=None, password=None, type=None):
        """
        Class providing credentials; if auth is enabled for a view, the credentials object will be added under request.auth
        """
        self.username = username
        self.password = password
        # the type of authentication used (e.g. 'Basic')
        self.type = type



class AuthHandler:
    def wrap(self, view):
        """
        Wraps a view in a wrapper for the specific auth
        """
        if not view.auth:
            # if no authentication is required nothing needs to be wrapped
            return view

        match view.auth.lower():
            case 'basic':
                # wrap in basic auth
                return self.wrap_basic(view)
            case other:
                # auth is not supported or does simply not exist
                log.error(f'view {view.target} HAS UNKNOWN AUTH TYPE')
                return error(500)

    def wrap_basic(self, view):
        """
        Wraps the view function (view.func) for basic authentication
        """

        # use reference to view before it was changed to the wrapper to avoid endless recursion
        func = view.func

        def wrapper(request, dynamic_params=None):
            # get authorization header
            authorization = request.headers.authorization
            # check if request has credentials, otherwise return 401 (Unauthorized)
            if not authorization or not authorization.startswith('Basic'):
                response = error(401)
            # gather credentials from request
            else:
                # get creds from auth header
                encoded_credentials = authorization.strip().split(' ')[1].strip()
                # creds are usually base64 encoded
                credentials = str(base64.b64decode(encoded_credentials), 'utf-8')
                username, password = credentials.split(':')
                # add credentials to request
                request.auth = Credentials(username=username, password=password, type='Basic')

                # get response from view
                response = func(request, dynamic_params)

            response.headers.WWW_Authenticate = 'Basic realm="Auth required to access resource"'
            return response
        # only wrap view.func not the actual view
        view.func = wrapper
        return view
