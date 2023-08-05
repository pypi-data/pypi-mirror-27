import os
import yaml

from copy import deepcopy

from .utils import ObjectDict

FILENAME = 'reliz.yml'

DEFAULTS = {
    'DEBUG': False,
    'DB': 'reliz.db',
    'SECRET_KEY': 'vPOF9nkSINcdMz56XxVEGmc0DVJsOHc5hrJfC6NXtzI=',
}


def load(home=None, **kwargs):
    config = ObjectDict(deepcopy(DEFAULTS))
    if home:
        filename = os.path.join(home, FILENAME)
        if os.path.exists(filename):
            with open(filename) as f:
                data = yaml.load(f.read())
                config.update(data)

    config.update(kwargs)
    return config


def init(app):
    app['config'] = load()
