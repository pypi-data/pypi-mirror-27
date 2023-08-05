# -*- coding: utf-8 -*-
import logging

from uuid import uuid4

from tinydb import TinyDB, Query
from tinydb.storages import MemoryStorage

from .errors import ValidationError
# from .validator import Validator, DocumentError

log = logging.getLogger(__name__)

query = Query()


class Manager(object):
    __table__ = None
    __schema__ = None

    def __init__(self, app, debug=False):
        self.app = app
        self.db = app.db
        self.table = self.db.table(self.__table__)

    def validate(self, data):
        v = self.__schema__()
        result = v.load(data)
        if result.errors:
            raise ValidationError(result.errors)
        # try:
        #     if v(data):
        #         return v.document
        #     else:
        #         raise ValidationError(
        #             'Validation failed for {0}'.format(self.__table__),
        #             v.errors
        #         )
        # except DocumentError as e:
        #     raise ValidationError('Data does not have the right format')

    @property
    def validation_error(self):
        return self.validator.errors

    def list(self, **kwargs):
        return self.table.all()

    def create(self, **data):
        id = uuid4().hex
        log.debug('Creating %s(%s)', self.__table__, id)
        data.update(id=id)
        self.table.insert(self.validate(data))
        return self.get(id)

    def get(self, id):
        workspaces = self.table.search(query.id == id)
        if len(workspaces) > 1:
            pass  # TODO: raise exception
        elif len(workspaces) == 0:
            pass  # TODO: raise exception
        else:
            return workspaces[0]

    def update(self, id, **kwargs):
        log.debug('Updating %s(%s)', self.__table__, id)
        self.table.update(kwargs, query.id == id)
        return self.get(id)

    def delete(self, id):
        log.debug('Deleting %s(%s)', self.__table__, id)
        self.table.remove(query.id == id)


async def middleware_factory(app, handler):
    async def middleware(request):
        if request.path.startswith('/static/') or request.path.startswith('/_debugtoolbar'):
            response = await handler(request)
            return response

        request.db = app.db
        response = await handler(request)
        return response
    return middleware


def init(app, debug=False):
    config = app.get('config', {})
    DB = config.get('DB')
    if isinstance(DB, str):
        db = TinyDB(DB)
    elif isinstance(DB, TinyDB):
        db = DB
    else:
        db = TinyDB(storage=MemoryStorage)
    app.db = app['db'] = db
