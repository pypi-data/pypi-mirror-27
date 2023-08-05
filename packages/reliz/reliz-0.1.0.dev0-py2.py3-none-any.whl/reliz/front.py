import asyncio
import os

import jinja2

from aiohttp import web

import aiohttp_jinja2
import aiohttp_debugtoolbar
from aiohttp_debugtoolbar import toolbar_middleware_factory

STATIC_PREFIX = '/static'
STATIC_PATH = os.path.join(os.path.dirname(__file__), 'static')
TEMPLATES_PATH = os.path.join(os.path.dirname(__file__), 'templates')

app = web.Application(middlewares=[toolbar_middleware_factory])
aiohttp_debugtoolbar.setup(app)


def static(filename):
    return STATIC_PREFIX + '/' + filename


@aiohttp_jinja2.template('index.html')
def index(request):
    return {'name': 'Andrew', 'surname': 'Svetlov'}


def init(app, debug=False):
    jinja_env = aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader(TEMPLATES_PATH))
    jinja_env.globals['static'] = static

    app.router.add_static(STATIC_PREFIX, STATIC_PATH, name='static')
    app.router.add_route('GET', '/{tail:.*}', index, name='index')
