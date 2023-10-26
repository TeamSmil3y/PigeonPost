import json

SUPPORTED_MIMETYPES = {
    'application/json': application_json,
}


def parse_body(content_type: str, header_params: dict, body: str):
    content_type, params = content_type.split(';', 1)
    if content_type in SUPPORTED_MIMETYPES:
        return SUPPORTED_MIMETYPES[content_type](header_params, body)

def application_json(header_params, body:str):
    return json.loads(body)