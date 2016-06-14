#!/usr/bin/env python
# coding=utf-8
import os
from aiohttp import web
from letsvote import setup
import config

application = app = web.Application()
setup(app)

if __name__ == '__main__':
    web.run_app(app, host=config.HOST, port=config.PORT, ssl_context=config.ssl_context)
