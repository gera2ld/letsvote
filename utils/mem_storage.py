#!/usr/bin/env python
# coding=utf-8
import uuid
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
