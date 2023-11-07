import pigeon.conf
from typing import Callable
from typing import Any
from urllib.parse import parse_qs, unquote_plus
from email import message_from_string
from pigeon.http import HTTPRequest, HTTPResponse


def autogenerator(view: Callable) -> Callable:
    """
    Wraps a view so that any responses generated from the view will have automatic type conversion.
    """

    # use reference to view before it was changed to the wrapper to avoid endless recursion
    func = view.func

    def wrapper(request, dynamic_params=None):
        # get response from view
        response = func(request, dynamic_params)
        # automatic type conversion
        return generate(response, view.mimetype)
    # only wrap view.func not the actual view
    view.func = wrapper
    return view


def generate(data: Any, mimetype=None) -> HTTPResponse:
    """
    Generates a valid HTTPResponse from returned view data (automatic type conversion).
    Untyped views may return str or HTTPResponse,
    typed views may return str, HTTPResponse or any type that can be converted
    into a valid HTTPResponse by the generator.
    """
    # view returned HTPResponse -> nothing to be generated
    if isinstance(data, HTTPResponse):
        return data
    
    # generators parse response data into str -> if the data is already of type str, we do not need to parse them
    if not isinstance(data, str) and (generator := pigeon.conf.settings.MIME_GENERATORS.get(mimetype)):
        data = generator.generate(data)
        
    # cannot send data if it is str
    if not isinstance(data, str):
        raise ValueError
    
    return HTTPResponse(data=data)


def parse(request: bytes) -> HTTPRequest:
    """
    Parses a bytes representation of an http request and creates a valid HTTPRequest object from it.
    """

    # decode request
    request = str(request, 'ascii')

    # split into request line and message
    request_line, message_raw = (request.split('\r\n', 1)+[''])[:2]

    # split into method, resource and protocol
    method, resource, protocol = request_line.split(' ')
    protocol = protocol.split('/')[1]
    # split resource locator into path and get params
    path, get_raw = (resource.split('?') + [''])[:2]
    path = unquote_plus(path)
    # parse get params and create dict from it
    get = parse_qs(get_raw)
    for key, value in get.items():
        if len(value) <=1: get[key] = get[key][0]

    # generate email.message.Message object to allow parsing of headers and body
    message = message_from_string(message_raw)
    # parse headers
    headers = {name: value for name, value in message.items()}

    # parse data
    mime_type = message.get_content_type()
    data = message.get_payload()
    files = dict()
    if mime_type in pigeon.conf.settings.MIME_PARSERS:
        # parser returns either DATA or (DATA, FILES)
        parsed = pigeon.conf.settings.MIME_PARSERS[mime_type].parse(data, message)
        if isinstance(parsed, (list, tuple)):
            # parser returned data and files
            data = parsed[0]
            files = parsed[1]
        else:
            # parser returned only data
            data = parsed

    return HTTPRequest(method=method, path=path, headers=headers, get=get, data=data, files=files, protocol=protocol)
