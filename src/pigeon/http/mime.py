from email.message import Message
from urllib.parse import parse_qs
import json


class JSONParser:
    @classmethod
    def parse(cls, data: str, msg: Message = None):
        return json.loads(data)


class MultiPartFormParser:
    @classmethod
    def parse(cls, data: str, msg: Message):
        parsed_data = {}
        parsed_files = {}
        for msg in msg.get_payload():
            # get content-disposition name and filename
            name = msg.get_param('name', header='Content-Disposition')
            filename = msg.get_filename()

            payload = msg.get_payload()
            if filename:
                _data = payload if not filename else [filename, payload]
                _dict = parsed_files
            else:
                _data = payload
                _dict = parsed_data

            # add file to parsed_files
            if name in _dict:
                # entry already exists for name (add to it)
                if isinsance(_dict[name], (list, tuple)):
                    _dict[name].append(_data)
                else:
                    _dict[name] = [_dict[name], _data]
            else:
                # make new entry in the dict
                _dict[name] = _data

        return parsed_data, parsed_files


class UrlencodedFormParser:
    @classmethod
    def parse(cls, data: str, msg: Message = None):
        return parse_qs(data)
