from pigeon.http import error, HTTPRequest, HTTPResponse
from typing import Any
import pigeon.utils.logger as logger
import base64

log = logger.Log('Auth', '#ff4a65')


class AuthHandler:
    def creds(self, request: HTTPRequest, auth_required: str | None) -> Any | None:
        """
        Returns credentials for a reuqest
        """
        if not auth_required:
            log.debug('NO AUTH REQUIRED - SKIPPING REQUEST')
        
        match auth_required.lower():
            case 'basic':
                authorization = request.headers('authorization')
                if not authorization:
                    log.warning('REQUEST IS LACKING BASIC AUTH')
                    # unauthorized -> tells browser to send credentials
                    response = error(401)
                else:
                    # get creds from auth header
                    encoded_credentials = authorization.strip().split(' ')[1].strip()
                    # creds are usually base64 encoded
                    credentials = str(base64.b64decode(encoded_credentials), 'utf-8')
                    log.debug(f'RECEIVED BASIC AUTH: {credentials}')
                    return credentials

        log.critical(f'REQUIRED AUTH {auth_required} IS NOT SUPPORTED OR DOES NOT EXIST')
        return response
        
    def evaluate(self, request: HTTPRequest, response: HTTPResponse, auth_required: str | None) -> HTTPResponse:
        """
        Evaluats a request and the corresponding response to check whether any required authentication is met.
        """
        # if no auth is required we can skip evaluating auth (duh!)
        if not auth_required:
            log.debug('NO AUTH REQUIRED - SKIPPING EVALUATION')
            return response
        
        match auth_required.lower():
            case 'basic':
                response.HEADERS['WWW-Authenticate'] = 'Basic realm="Auth required to access resource"'
                return response
            case other:
                # 
                log.critical(f'REQUIRED AUTH {other} IS NOT SUPPORTED OR DOES NOT EXIST')
                return error(500)
        
        return response