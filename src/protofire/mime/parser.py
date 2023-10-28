
def parse(data, main_content_type, sub_content_type):
    if mime_type in SUPPORTED_MIMETYPES:
        return SUPPORTED_MIMETYPES[mime_type](data)
    else:
        return data
    

SUPPORTED_MAIN_MIMETYPES = {
    'application/json': application_json,
    'application/x-www-form-urlencoded': application_form_urlencoded,
}
