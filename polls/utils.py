import json
from functools import wraps
from tornado.httpclient import AsyncHTTPClient, HTTPError

async def load_user_from_token(application, authorization):
    url = application.settings['ARBITER_URL'] + '/api/user'
    headers = {
        'Authorization': authorization,
    }
    client = AsyncHTTPClient()
    try:
        res = await client.fetch(url, headers=headers)
        return json.loads(res.body)
    except HTTPError as e:
        if e.code >= 500: raise e

def require_token(allow_anonymous=False):
    def wrapper(handle):
        @wraps(handle)
        async def wrapped(self, *k, **kw):
            authorization = self.request.headers.get('AUTHORIZATION')
            user = None
            if authorization:
                try:
                    user = await load_user_from_token(self.application, authorization)
                except Exception as exc:
                    self.set_status(500)
                    self.write({
                        'error': repr(exc),
                    })
                    return
            if user is None and not allow_anonymous:
                self.set_status(401)
                self.write({
                    'error': 'Invalid token',
                    'log_in': self.application.settings['ARBITER_URL'],
                })
                return
            self.user = user or {}
            return handle(self, *k, **kw)
        return wrapped
    return wrapper

def pick_keys(data, keys):
    res = {}
    for k in keys:
        v = data.get(k)
        if v is not None:
            res[k] = v
    return res
