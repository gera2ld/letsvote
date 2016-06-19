#!/usr/bin/env python
# coding=utf-8
import asyncio
import aiohttp_session.redis_storage

async def init_redis_pool():
    import aioredis
    return await aioredis.create_pool(('127.0.0.1', 6379))

HOST = ''
PORT = 3002
ssl_context = None

# MemoryStorage
# import utils.mem_storage
# redis_pool = utils.mem_storage.MockRedisPool()
# session_storage = utils.mem_storage.MemoryStorage()

# RedisStorage
redis_pool = asyncio.get_event_loop().run_until_complete(init_redis_pool())
session_storage = aiohttp_session.redis_storage.RedisStorage(redis_pool)

login = {
    'github': {
        'client_id': 'CLIENT_ID',
        'client_secret': 'CLIENT_SECRET',
    }
}
