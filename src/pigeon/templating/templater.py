from pigeon.conf import Manager
from pigeon.http import HTTPResponse
from jinja2 import Environment, FileSystemLoader, select_autoescape
import mimetypes


env = None


def load():
    global env
    env = Environment(
        loader=FileSystemLoader(searchpath=Manager.templates_dir),
        autoescape=select_autoescape(),
    )


def render(template, context: dict, status: int=200) -> HTTPResponse:
    # get mimetype for file
    mimetype = mimetypes.guess_type(Manager.templates_dir / template)[0]
    global env
    rendered = env.get_template(template).render(**context)
    return HTTPResponse(headers={'Content-Type': mimetype}, data=rendered, status=status)
