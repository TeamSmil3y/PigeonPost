import json


# /json
def parse_json(data):
    return json.loads(data)


# /x-www-form-urlencoded
def parse_x_www_form_urlencoded(data):
    return {param[0]: param[1] for param in [_param.split('=', 1) for _param in data[1:].split('&')]}