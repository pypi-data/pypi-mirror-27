import logging

import click

from .utils import color, yellow, red, cyan, white, ARROW, DEBUG


LEVEL_COLORS = {
    logging.WARNING: yellow,
    logging.ERROR: red,
    logging.CRITICAL: color('black', bg='red', bold=True),
}


class CliFormatter(logging.Formatter):
    """
    Convert a `logging.LogRecord' object into colored text, using ANSI
    escape sequences.
    """
    def format(self, record):
        record.msg = str(record.msg).replace('\n', '\n  │ ')
        record.msg = ' '.join((self._prefix(record), record.msg))
        return super().format(record)

    def formatException(self, ei):
        '''Indent traceback info for better readability'''
        out = super().formatException(ei)
        out = '\n'.join('  │ ' + line for line in out.splitlines())
        return out

    def _prefix(self, record):
        if record.levelno == logging.INFO:
            return cyan(ARROW)
        if record.levelno == logging.DEBUG:
            return cyan(DEBUG)
        else:
            color = LEVEL_COLORS.get(record.levelno, white)
            return '{0}:'.format(color(record.levelname.upper()))


class CliHandler(logging.Handler):
    def emit(self, record):
        try:
            msg = self.format(record)
            err = record.levelno >= logging.WARNING
            click.echo(msg, err=err)
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            self.handleError(record)


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


def init_devserver_logging():
    from aiohttp_devtools.logs import DefaultHandler
    # create logger
    logger = logging.getLogger('relize')
    logger.setLevel(logging.DEBUG)

    # create console handler and set level to debug
    handler = logging.StreamHandler()
    handler = DefaultHandler()
    handler.setLevel(logging.DEBUG)

    # create formatter
    formatter = logging.Formatter('[%(asctime)s] %(name)s - %(levelname)s - %(message)s', datefmt='%H:%M:%S')

    # add formatter to handler
    handler.setFormatter(formatter)

    # add handler to logger
    logger.addHandler(handler)


def init_logging(verbose=False):
    logger = logging.getLogger()
    handler = CliHandler()
    handler.setFormatter(CliFormatter())
    logger.addHandler(handler)

    logger.setLevel(logging.DEBUG if verbose else logging.INFO)

    # Hide watchdog logging
    logging.getLogger('watchdog').setLevel(logging.WARNING)
