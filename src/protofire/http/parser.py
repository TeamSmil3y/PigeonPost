import mime_parsers as parser
from email import message_from_string
from email.message import Message


def parse_raw(message_raw):
    # generate email.message.Message object to allow parsing of headers and body
    message = message_from_string(message_raw)
    # parse headers
    headers = {name: value for name, value in message.items()}
    # parse body
    payload = _resolve_payload(message.get_payload(), mime_type=message.get_content_type())

    return headers, payload


def _resolve_payload(payload, mime_type):
    if isinstance(payload, (list, tuple)):
        return [_resolve_payload(_payload, mime_type) for _payload in payload]
    elif isinstance(payload, Message):
        # is multipart
        return _resolve_payload(payload.get_payload(), payload.get_content_disposition())
    else:
        return parser.parse(payload, mime_type)