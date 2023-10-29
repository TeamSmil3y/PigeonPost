from email.message import Message
import protofire.mime.parsers as parsers

def parse(msg: Message):
    """
    Parses the body of an email.message.Message object.
    The mime-type of the body is determined using the content-type header.
    If there is no mime-type for a given parser, the body is simply returned as string.
    """
    mime_type = msg.get_content_type()
    data = msg.get_payload()
    if mime_type in SUPPORTED_MIMETYPES:
        # parser returns either DATA or (DATA, FILES)
        parsed = SUPPORTED_MIMETYPES[mime_type].parse(data, msg)
        if isinstance(parsed, (list, tuple)):
            # parser returned (DATA, FILES)
            return parsed[0], parsed[1]
        else:
            # parser returned (DATA)
            return parsed, dict()
    else:
        # no parser found
        return data, dict()


SUPPORTED_MIMETYPES = {
    'application/json': parsers.JSONParser,
    'application/x-www-form-urlencoded': parsers.UrlencodedFormParser,
    'multipart/form-data': parsers.MultiPartFormParser,
}
