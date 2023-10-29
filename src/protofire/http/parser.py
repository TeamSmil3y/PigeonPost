import protofire.http.mime as mime
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
    mime_type = msg.get_content_type()
    data = msg.get_payload()
    files = dict()
    if mime_type in SUPPORTED_MIMETYPES:
        # parser returns either DATA or (DATA, FILES)
        parsed = SUPPORTED_MIMETYPES[mime_type].parse(data, msg)
        if isinstance(parsed, (list, tuple)):
            # parser returned data and files
            data = parsed[0]
            files = parsed[1]
        else:
            # parser returned only data
            data = parsed

    return method, path, get, protocol, headers, data, files
