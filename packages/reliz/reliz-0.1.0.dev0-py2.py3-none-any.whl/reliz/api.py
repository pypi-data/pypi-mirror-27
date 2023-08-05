import json

import aiohttp_cors

from aiohttp import web
# from docker import APIClient

# docker = APIClient(base_url='unix://var/run/docker.sock')


_routes = []


def route(path, name=None):
    def wrapped(cls):
        _routes.append(('/api/1{0}'.format(path), cls, name))
        return cls
    return wrapped


class Api(web.View):
    pass
    # async def json(self, data):
    #     body = json.dumps(data).encode('utf-8')
    #     return web.Response(body=body, content_type="application/json")


# @route('/docker/images', 'docker-images')
# class DockerImages(Api):
#     async def get(self):
#         return self.json(docker.images())
#
#
# @route('/jobs', 'jobs')
# class JobsApi(Api):
#     async def get(self):
#         data = {
#             'items': self.request.app.jobs.list()
#         }
#         return web.json_response(data)
#
#
# @route('/workspaces', 'workspaces')
# class WorkspacesApi(Api):
#     @property
#     def workspaces(self):
#         return self.request.app.workspaces
#
#     async def get(self):
#         data = {
#             'items': self.workspaces.list()
#         }
#         return web.json_response(data)
#
#     async def post(self):
#         data = await self.request.json()
#         workspace = self.workspaces.create(**data)
#         return web.json_response(workspace)
#
#
# @route('/workspaces/{id}', 'workspace')
# class WorkspaceApi(Api):
#     @property
#     def workspaces(self):
#         return self.request.app.workspaces
#
#     async def get(self):
#         id = self.request.match_info['id']
#         workspace = self.workspaces.get(id)
#         return web.json_response(workspace)
#
#     # async def post(self):
#     #     if self.request.has_body:
#     #         data = await self.request.json()
#     #     else:
#     #         data = {}
#     #     id = self.request.match_info['id']
#     #     workspace = await self.workspaces.launch(id, **data)
#     #     return web.json_response(workspace)
#
#
# @route('/pipelines', 'pipelines')
# class PipelinesApi(Api):
#     @property
#     def pipelines(self):
#         return self.request.app.pipelines
#
#     async def get(self):
#         data = {
#             'items': self.pipelines.list()
#         }
#         return web.json_response(data)
#
#     async def post(self):
#         data = await self.request.json()
#         pipeline = self.pipelines.create(**data)
#         return web.json_response(pipeline)
#
#
# @route('/pipelines/{id}', 'pipeline')
# class PipelinesApi(Api):
#     @property
#     def pipelines(self):
#         return self.request.app.pipelines
#
#     async def get(self):
#         id = self.request.match_info['id']
#         pipeline = self.pipelines.get(id)
#         return web.json_response(pipeline)
#
#     async def post(self):
#         if self.request.has_body:
#             data = await self.request.json()
#         else:
#             data = {}
#         id = self.request.match_info['id']
#         pipeline = await self.pipelines.launch(id, **data)
#         return web.json_response(pipeline)


def init(app, debug=False):
    cors = aiohttp_cors.setup(app)

    for path, cls, name in _routes:
        app.router.add_route('*', path, cls, name=name)
