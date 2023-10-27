import protofire.http.http as http
import json


def parse_body(content_type: str, header_params: dict, body: str):
    if content_type in SUPPORTED_MIMETYPES:
        return SUPPORTED_MIMETYPES[content_type](header_params, body)
    print('UNSUPPORTED MIME TYPE')


def application_json(header_params, body: str):
    return json.loads(body)

def form_data(header_params, body:str):
    return {param[0]:param[1] for param in [_param.split('=', 1) for _param in body[1:].split('&')]}

def multipart_form_data(header_params, body: str):
    if 'boundary' in header_params['Content-Type']:
        boundary = header_params['Content-Type']['boundary']
        sections = [section.strip() for section in body.split(boundary)[1:-1]]
        for section in sections:
            header_str, body_str = section.split('\r\n\r\n')
            header_lines, headers, header_params = http.HttpObject._parse_headers(header_str)
            print('HEADERS: ', headers, header_params, body)
            body = parse_body(headers['Content-Type'], headers, body_str)



SUPPORTED_MIMETYPES = {
    'application/json': application_json,
    'multipart/form-data': multipart_form_data,
    'form-data': form_data,
}
