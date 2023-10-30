import pigeon.http.mime as mime
import pigeon.conf.settings as _settings
from urllib.parse import parse_qs, unquote_plus
from email import message_from_string
from email.message import Message


def parse(request: str):
    """
    Parses an entire HTTP request
    """
    settings = _settings.get()

    # split into request line and message
    request_line, message_raw = (request.split('\r\n', 1)+[''])[:2]

    # split into method, resource and protocol
    method, resource, protocol = request_line.split(' ')
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
    if mime_type in settings.supported_mimetypes:
        # parser returns either DATA or (DATA, FILES)
        parsed = settings.supported_mimetypes[mime_type].parse(data, message)
        if isinstance(parsed, (list, tuple)):
            # parser returned data and files
            data = parsed[0]
            files = parsed[1]
        else:
            # parser returned only data
            data = parsed

    return method, path, get, protocol, headers, data, files
