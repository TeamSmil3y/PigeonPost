from pigeon.conf import settings
from pigeon.http import HTTPResponse
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, select_autoescape
import mimetypes


env = None


def load():
    global env
    env = Environment(
        loader=FileSystemLoader(searchpath=settings.TEMPLATES_DIR),
        autoescape=select_autoescape(),
    )


def render(template, context, status=200):
    # get mimetype for file
    mimetype = mimetypes.guess_type(settings.TEMPLATES_DIR / template)[0]
    global env
    rendered = env.get_template(template).render(**context)
    return HTTPResponse(headers={'Content-Type': mimetype}, data=rendered, status=status)
