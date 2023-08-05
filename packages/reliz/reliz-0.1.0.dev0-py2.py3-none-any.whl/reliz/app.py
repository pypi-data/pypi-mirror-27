import asyncio
import logging
import os
import re

import uvloop
import click


from aiohttp import web

from aiohttp_session import get_session, session_middleware
from aiohttp_session.cookie_storage import EncryptedCookieStorage

from . import config, db, api, errors, front
# , ws, worker, jobs, pipeline, workspace

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


class App(web.Application):
    pass


def create(conf, debug=False, loop=None, **kwargs):
    loop = loop or asyncio.get_event_loop()
    conf.update(kwargs)
    middlewares = [
        errors.middleware,
        session_middleware(EncryptedCookieStorage(conf.SECRET_KEY)),
        db.middleware_factory,
    ]

    app = App(loop=loop, middlewares=middlewares, debug=debug)
    app['config'] = conf
    # config.init(app, debug)
    db.init(app, debug)
    api.init(app, debug)
    # ws.init(app, debug)
    front.init(app, debug)
    # jobs.init(app, debug)
    # pipeline.init(app, debug)
    # workspace.init(app, debug)
    # worker.init(app, debug)

    return app


class DevServerLogHandler(logging.Handler):
    prefix = click.style('⇨', fg='blue')

    def emit(self, record):

        log_entry = self.format(record)
        color = 'white'
        # colour = LOG_COLOURS.get(record.levelno, 'red')
        m = re.match('^(\[.*?\] )', log_entry)
        time = click.style(m.groups()[0], fg='magenta')
        msg = log_entry[m.end():]
        if record.levelno == logging.INFO and msg.startswith('>'):
            msg = '{prefix} {msg}'.format(prefix=self.prefix, msg=msg[2:])
        else:
            msg = click.style(msg, fg=color)
        click.echo(time + msg)


def devserver(loop):
    from aiohttp_devtools.logs import DefaultHandler
    # create logger
    logger = logging.getLogger('reliz')
    logger.setLevel(logging.DEBUG)

    # create console handler and set level to debug
    ch = logging.StreamHandler()
    ch = DefaultHandler()
    ch.setLevel(logging.DEBUG)

    # create formatter
    formatter = logging.Formatter('[%(asctime)s] %(name)s - %(levelname)s - %(message)s', datefmt='%H:%M:%S')

    # add formatter to ch
    ch.setFormatter(formatter)

    # add ch to logger
    logger.addHandler(ch)

    conf = config.load(os.environ.get('RELIZ_HOME'), debug=True, verbose=True)
    return create(conf, debug=True, loop=loop)
