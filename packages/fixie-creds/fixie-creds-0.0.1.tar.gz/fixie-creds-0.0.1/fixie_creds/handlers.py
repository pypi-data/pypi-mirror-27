"""Tornado handlers for interfacing with fixie credentials."""

from fixie.request_handler import RequestHandler

from fixie_creds.cache import CACHE


class Register(RequestHandler):

    schema = {'user': {'type': 'string', 'empty': False},
              'email': {'type': 'string', 'empty': False},
              }

    def post(self):
        token, flag = CACHE.register(**self.request.arguments)
        if flag:
            response = {'token': token, 'status': True}
        else:
            response = {'token': '<not-a-token>', 'status': False, 'message': token}
        self.write(response)


class Verify(RequestHandler):

    schema = {'user': {'type': 'string', 'empty': False},
              'token': {'type': 'string', 'regex': '[0-9a-fA-F]+'},
              }
    response_keys = ('verified', 'message', 'status')

    def post(self):
        resp = CACHE.verify(**self.request.arguments)
        response = dict(zip(self.response_keys, resp))
        self.write(response)


class Deregister(RequestHandler):

    schema = {'user': {'type': 'string', 'empty': False},
              'token': {'type': 'string', 'regex': '[0-9a-fA-F]+'},
              }
    response_keys = ('message', 'status')

    def post(self):
        resp = CACHE.deregister(**self.request.arguments)
        response = dict(zip(self.response_keys, resp))
        self.write(response)


class Reset(RequestHandler):

    schema = {'user': {'type': 'string', 'empty': False},
              'email': {'type': 'string', 'empty': False},
              }

    def post(self):
        token, flag = CACHE.reset(**self.request.arguments)
        if flag:
            response = {'token': token, 'status': True}
        else:
            response = {'token': '<not-a-token>', 'status': False, 'message': token}
        self.write(response)


HANDLERS = [
    ('/verify', Verify),
    ('/register', Register),
    ('/deregister', Deregister),
    ('/reset', Reset),
]