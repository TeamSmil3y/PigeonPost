import pigeon.conf.settings as _settings
from pigeon.http import HTTPResponse
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, select_autoescape
import mimetypes
import os

env = None


def load():
    settings = _settings.get()
    global env
    env = Environment(
        loader=FileSystemLoader(searchpath=settings.templates_dir),
        autoescape=select_autoescape(),
    )


def render(template, context, status=200):
    # get mimetype for file
    settings = _settings.get()
    mimetype = mimetypes.guess_type(settings.templates_dir / template)[0]
    global env
    rendered = env.get_template(template).render(**context)
    return HTTPResponse(headers={'Content-Type':mimetype}, data=rendered, status=status)