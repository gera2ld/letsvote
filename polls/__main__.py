import tornado.web
import tornado.ioloop
from . import settings
from .handlers import handlers

application = tornado.web.Application(handlers, **settings.as_dict())

if settings.UNIX_SOCKET is not None:
    from tornado.httpserver import HTTPServer
    from tornado.netutil import bind_unix_socket
    server = HTTPServer(application)
    socket = bind_unix_socket(settings.UNIX_SOCKET, mode=0o777)
    server.add_socket(socket)
else:
    application.listen(settings.PORT)

tornado.ioloop.IOLoop.current().start()
