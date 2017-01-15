import tornado.web
import tornado.ioloop
from . import settings
from .handlers import handlers
from .settings import PORT

application = tornado.web.Application(handlers, **settings.as_dict())
application.listen(PORT)
tornado.ioloop.IOLoop.current().start()
