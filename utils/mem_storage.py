#!/usr/bin/env python
# coding=utf-8
import uuid, time, pickle
from aiohttp_session import AbstractStorage, Session

class MemoryStorage(AbstractStorage):
    def __init__(self, *, cookie_name="AIOHTTP_SESSION",
            domain=None, max_age=None, path='/',
            secure=None, httponly=True):
        super().__init__(cookie_name=cookie_name, domain=domain,
                max_age=max_age, path=path, secure=secure,
                httponly=httponly)
        self.data = {}

    async def load_session(self, request):
        cookie = self.load_cookie(request)
        if cookie is not None:
            key = str(cookie)
            data = self.data.get(key)
            if data is None: key = None
        else:
            key = data = None
        return Session(key, data=data, new=key is None)

    async def save_session(self, request, response, session):
        key = session.identity
        if key is None:
            key = uuid.uuid4().hex
        else:
            key = str(key)
        self.save_cookie(response, key, max_age=session.max_age)
        self.data[key] = self._get_session_data(session)

class MockRedis:
    def __init__(self, data):
        self.data = data

    async def get(self, key):
        item = self.data.get(key)
        if item is not None:
            if item['expire'] < time.time():
                self.data.pop(key)
                item = None
        if item is not None:
            return pickle.loads(item['value'])

    async def set(self, key, val, expire=None):
        if expire is None:
            expire = time.time() + 60
        self.data[key] = {
            'value': pickle.dumps(val),
            'expire': expire,
        }

class MockRedisPool:
    def __init__(self):
        self.data = {}
        self.redis = MockRedis(self.data)

    def __enter__(self):
        return self.redis

    def __exit__(self, *k):
        pass

    def __iter__(self):
        if False: yield self    # make an generator
        return self

    __await__ = __iter__ # make compatible with 'await' expression
