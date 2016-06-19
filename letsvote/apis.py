#!/usr/bin/env python
# coding=utf-8
import json
import aiohttp
from .models import *

class HTTPUnprocessableEntity(aiohttp.web.HTTPClientError):
    status_code = 422

def on_prepare(request, response):
    if not request.path.startswith('/api/'): return
    if request is not None:
        origin = request.headers.get('origin')
    else:
        origin = None
    if origin is not None:
        response.headers['Access-Control-Allow-Origin'] = origin
        response.headers['Vary'] = 'Origin'
    # else:
    #     response.headers['Access-Control-Allow-Origin'] = '*'

async def get_user(request):
    user = None
    token = request.GET.get('token')
    if token is None:
        token = request.headers.get('Authorization')
    if token is not None:
        with await request.app.config.redis_pool as redis:
            user = await redis.get('user_token:' + str(token))
    if user is None: user = {}
    return user.get('user_id'), user.get('user_name')

def safe_get_poll(vid, user_id):
    poll = Poll.load(vid, user_id)
    if poll is None:
        api_not_found()
    return poll

def dumps(data):
    return json.dumps(data, separators = (',', ':'), ensure_ascii = False)

def api(handle):
    async def handler(request):
        data = await handle(request)
        return aiohttp.web.json_response(data, dumps=dumps)
    return handler

def api_error(msg = None, error_class = aiohttp.web.HTTPServiceUnavailable,
        data = None):
    exc = error_class(content_type='application/json')
    if data is None:
        data = {
            'status': exc.status,
            'reason': msg or exc.reason,
        }
    exc.text = dumps(data)
    raise exc

def api_not_found(msg=None):
    api_error(msg, error_class=aiohttp.web.HTTPNotFound)

@api
async def handle_get_detail(request):
    user_id, user_name = await get_user(request)
    poll = safe_get_poll(request.match_info['vid'], user_id)
    return poll.to_json()

@api
async def handle_post_detail(request):
    user_id, _ = await get_user(request)
    poll = safe_get_poll(request.match_info['vid'], user_id)
    data = await request.post()
    oids = data.getall('voteGroup')
    try:
        poll.vote(oids)
    except AlreadyVoted:
        api_error('Already voted!', error_class=HTTPUnprocessableEntity)
    return poll.to_json()

@api
async def handle_post_create(request):
    user_id, _ = await get_user(request)
    payload = await request.post()
    data = {
        'user_id': user_id,
        'title': payload['title'],
        'desc': payload['desc'],
        'options': payload.getall('option'),
    }
    try:
        poll = Poll.create(data)
    except:
        import traceback
        traceback.print_exc()
        api_error('Invalid data!', error_class=HTTPUnprocessableEntity)
    else:
        return poll.to_json()
