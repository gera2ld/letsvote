#!/usr/bin/env python
# coding=utf-8
import os
import aiohttp_jinja2, jinja2
from . import handlers

ROOT = os.path.join(os.path.dirname(__file__), '..')

def setup(app):
    aiohttp_jinja2.setup(app,
        # extensions=['jinja2htmlcompress.HTMLCompress'],
        loader=jinja2.FileSystemLoader(os.path.join(ROOT, 'templates')))
    app.router.add_route('GET', '/{vid}', handlers.handle_get)
    app.router.add_route('POST', '/{vid}', handlers.handle_post)
    app.router.add_static('/static', os.path.join(ROOT, 'static'))
