#!/usr/bin/env python
# coding=utf-8
import urllib.parse
import aiohttp
from .models import User

class BadRequest(Exception): pass

handlers = {}
def callback(source):
    def wrapper(handler):
        async def handle(request):
            user_data = await handler(request)
            user_data['oauth_id'] = source + ':' + str(user_data['oauth_id'])
            user = User.update(user_data)
            return user
        handlers[source] = handle
        return handle
    return wrapper

async def handle(request):
    source = request.match_info['source']
    handler = handlers.get(source)
    if handler is not None:
        return await handler(request)

@callback('github')
async def handle_github(request):
    code = request.GET.get('code')
    # state = request.GET.get('state')
    if not code:
        raise BadRequest
    with aiohttp.ClientSession() as session:
        login = request.app.config.login.get('github')
        data = {
            'client_id': login['client_id'],
            'client_secret': login['client_secret'],
            'code': code,
        }
        async with session.post('https://github.com/login/oauth/access_token', data=data) as res:
            qs = await res.text()
            qs_data = urllib.parse.parse_qs(qs)
            token = qs_data['access_token'][0]
        params = {
            'access_token': token,
        }
        async with session.get('https://api.github.com/user', params=params) as res:
            user_data = await res.json()
            return {
                'oauth_id': user_data['id'],
                'name': user_data['name'],
                'email': user_data['email'],
                'avatar_url': user_data['avatar_url'],
                'gravatar_id': user_data['gravatar_id'],
                'token': token,
            }
