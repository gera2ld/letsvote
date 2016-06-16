#!/usr/bin/env python
# coding=utf-8
import asyncio
from . import api

loop = asyncio.get_event_loop()
loop.run_until_complete(api.test())
