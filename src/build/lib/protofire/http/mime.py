import json


def parse_body(content_type: str, header_params: dict, body: str):
    if content_type in SUPPORTED_MIMETYPES:
        return SUPPORTED_MIMETYPES[content_type](header_params, body)


def application_json(header_params, body: str):
    return json.loads(body)

def multipart_form_data(header_params, body: str):
    print(header_params['Content-Type'])
    if 'boundary' in header_params['Content-Type']:
        boundary = header_params['Content-Type']['boundary']
        boundary = boundary[:body.index(boundary)]
        sections = [section.strip() for section in body.split(boundary)[1:-1]]
        print(boundary, sections)


SUPPORTED_MIMETYPES = {
    'application/json': application_json,
    'multipart/form-data': multipart_form_data,
}
