import tornado.web
import tornado.ioloop
from . import settings
from .handlers import handlers
from .settings import UNIX_SOCKET, PORT

application = tornado.web.Application(handlers, **settings.as_dict())

if UNIX_SOCKET is not None:
    from tornado.httpserver import HTTPServer
    from tornado.netutil import bind_unix_socket
    server = HTTPServer(application)
    socket = bind_unix_socket(UNIX_SOCKET)
    server.add_socket(socket)
else:
    application.listen(PORT)

tornado.ioloop.IOLoop.current().start()
