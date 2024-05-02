import json
import sys
import traceback
from jinja2 import Environment, BaseLoader
from pigeon.conf import Manager
from pigeon.http.response import HTTPResponse
from pigeon.http.request import HTTPRequest

string_template = """
<style>
    body {
        background-color: black;
        color: white;
        margin: 0 2rem;
    }
    .head {
        padding: 2rem 1rem 0;
        font-family: Arial;
    }
    .status-code {
        color: #c74a4a;
    }
    .traceback {
        background-color: #141414;
        padding-left: 1.5rem;
        border-radius: 1rem;
    }
    .reminder {
        font-family: Arial;
        padding: 0 1rem;
    }
    .debug-mode {
        color: #c7bd4a;
    }
    
</style>
<h1 class="head">HTTP Status <span class="status-code">{{status}}</span></h1>
<pre class="traceback">
    <code>
        {{traceback}}
    </code>
</pre>
<h3 class="reminder">You are seeing this message because your application is running in <span class="debug-mode">DEBUG MODE</span></h3>
"""
debug_template = Environment(loader=BaseLoader()).from_string(string_template)


def fallback(request: HTTPRequest | None, code: int):
    """
    Fallback for when no specific error view is provided for status code
    """
    if 600>code>=500 and Manager.debug_mode:
        return HTTPResponse(data=debug_template.render(status=code, traceback=''.join(traceback.format_exception(type(sys.last_exc), sys.last_exc, sys.last_exc.__traceback__))), content_type='text/html', status=code)

    return HTTPResponse(data=json.dumps({'error': f'error{": " + request.path if request else ""} {code}'}), content_type='application/json', status=code)
