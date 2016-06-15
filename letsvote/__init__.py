#!/usr/bin/env python
# coding=utf-8
import os
import aiohttp_jinja2, jinja2
from . import handlers, apis

ROOT = os.path.join(os.path.dirname(__file__), '..')

def setup(app):
    aiohttp_jinja2.setup(app,
        # extensions=['jinja2htmlcompress.HTMLCompress'],
        loader=jinja2.FileSystemLoader(os.path.join(ROOT, 'templates')))
    app.on_response_prepare.append(apis.on_prepare)
    app.router.add_route('POST', '/api/votes', apis.handle_post_create)
    app.router.add_route('GET', '/api/votes/{vid}', apis.handle_get_detail)
    app.router.add_route('POST', '/api/votes/{vid}', apis.handle_post_detail)
    app.router.add_route('GET', '/', handlers.handle_get_create)
    app.router.add_route('POST', '/', handlers.handle_post_create)
    app.router.add_route('GET', '/{vid}', handlers.handle_get_detail)
    app.router.add_route('POST', '/{vid}', handlers.handle_post_detail)
    app.router.add_static('/static', os.path.join(ROOT, 'static'))
