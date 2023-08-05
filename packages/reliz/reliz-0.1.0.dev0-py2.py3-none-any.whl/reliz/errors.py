import logging

from aiohttp.web import json_response

log = logging.getLogger(__name__)

_errors = {

}


def handler(cls):
    '''Register an error handler for a given exception'''
    def wrapper(func):
        _errors[cls] = func
        return func
    return wrapper


class ValidationError(ValueError):
    def __init__(self, msg, errors=None):
        super().__init__(msg)
        self.msg = msg
        self.errors = errors


@handler(ValidationError)
async def validation_error(error):
    log.error('Validation error "%s": %s', error.msg, str(error.errors))
    return json_response({
        'message': error.msg,
        'errors': error.errors,
    }, status=400)


async def middleware(app, handler):
    async def middleware_handler(request):
        try:
            return await handler(request)
        except tuple(_errors.keys()) as e:
            error_handler = _errors[e.__class__]
            return await error_handler(e)
    return middleware_handler
