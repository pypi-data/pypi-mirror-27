# -*- coding: utf-8 -*-
import os

import click

from aiohttp.web import run_app

from . import app, config
from .utils import ObjectDict
from .templates import render_template
# from .log import init_logging


CONTEXT_SETTINGS = {
    'auto_envvar_prefix': 'RELIZ',
    'help_option_names': ['-?', '-h', '--help'],
}


def color(name, **kwargs):
    return lambda t: click.style(str(t), fg=name, **kwargs)


green = color('green', bold=True)
yellow = color('yellow', bold=True)
red = color('red', bold=True)
cyan = color('cyan')
magenta = color('magenta', bold=True)
white = color('white', bold=True)


OK = '✔'
KO = '✘'
WARNING = '⚠'


@click.group(context_settings=CONTEXT_SETTINGS)
@click.option('-d', '--debug', is_flag=True, help='Enable debug')
@click.option('-v', '--verbose', is_flag=True, help='Verbose output')
@click.option('-H', '--home',
              type=click.Path(file_okay=False, writable=True, resolve_path=True),
              help='The Reliz home directory')
@click.pass_context
def cli(ctx, verbose, debug, home, **kwargs):
    '''Reliz - Manage releases versionning accross multiple products'''
    # init_logging(verbose)
    # ctx.obj = config.load(debug=debug, verbose=verbose)
    ctx.obj = ObjectDict(
        home=home,
        config=config.load(home, debug=debug, verbose=verbose)
    )


@cli.command()
@click.pass_context
def init(ctx):
    '''Initialize a new Relize workspace'''
    home = ctx.obj.home
    click.echo(cyan('Creating Reliz home in {0}'.format(home)))
    if os.path.exists(home):
        if os.path.isdir(home):
            click.echo(yellow('{0} already exists, some content might be overrwritten.'.format(home)))
            click.confirm('Are you sure ?', abort=True)
        else:
            msg = red('{0} already exists and is not a directory'.format(home))
            click.echo(msg)
            raise click.Abort()
    os.makedirs(home, exist_ok=True)
    render_template('reliz.yml', os.path.join(home, 'reliz.yml'))


@cli.command()
@click.option('-d', '--debug', is_flag=True)
@click.option('--port', default=8000)
def serve(debug, port):
    '''Launch a development server'''
    click.echo(cyan('Serving on http://127.0.0.1:{0}/'.format(port)))
    application = app.create(debug)
    run_app(application, port=port)


@cli.command()
def dump():
    '''Dump configuration and jobs as JSON'''
    pass


@cli.command()
def load():
    '''Load configuration and jobs as JSON'''
    pass
