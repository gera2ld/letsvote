#!/usr/bin/env python
# coding=utf-8
import asyncio

async def init_redis_storage():
    import aioredis, aiohttp_session.redis_storage
    pool = await aioredis.create_pool(('127.0.0.1', 6379))
    return aiohttp_session.redis_storage.RedisStorage(pool)

HOST = ''
PORT = 3002
ssl_context = None

# MemoryStorage
# import utils.mem_storage
# session_storage = utils.mem_storage.MemoryStorage()

# RedisStorage
session_storage = asyncio.get_event_loop().run_until_complete(init_redis_storage())

login = {
    'github': {
        'client_id': 'CLIENT_ID',
        'client_secret': 'CLIENT_SECRET',
    }
}
