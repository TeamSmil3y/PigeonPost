import protofire.mime.mime as mime
from urllib.parse import parse_qs, unquote_plus
from email import message_from_string
from email.message import Message


def parse(request: str):
    """
    Parses an entire HTTP request
    """
    # split into request line and message
    request_line, message_raw = (request.split('\r\n', 1)+[''])[:2]

    # split into method, resource and protocol
    method, resource, protocol = request_line.split(' ')
    # split resource locator into path and get params
    path, get_raw = (resource.split('?') + [''])[:2]
    path = unquote_plus(path)
    # parse get params and create dict from it
    get = parse_qs(get_raw)

    # generate email.message.Message object to allow parsing of headers and body
    message = message_from_string(message_raw)
    # parse headers
    headers = {name: value for name, value in message.items()}
    # parse data
    data, files = mime.parse(message)

    return method, path, get, protocol, headers, data, files
