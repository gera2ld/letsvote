#!/usr/bin/env python
# coding=utf-8
import json
import aiohttp
from .models import *
from .utils import get_vote

class HTTPUnprocessableEntity(aiohttp.web.HTTPClientError):
    status_code = 421

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

def safe_get_vote(request):
    vote = get_vote(request)
    if vote is None:
        api_not_found()
    return vote

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
    vote = safe_get_vote(request)
    return vote.to_json()

@api
async def handle_post_detail(request):
    vote = safe_get_vote(request)
    data = await request.post()
    oids = data.getall('voteGroup')
    try:
        vote.vote(oids)
    except AlreadyVoted:
        api_error('Already voted!', error_class=HTTPUnprocessableEntity)
    return vote.to_json()

@api
async def handle_post_create(request):
    payload = await request.post()
    data = {
        'user_id': user_id(request),
        'title': payload['title'],
        'desc': payload['desc'],
        'options': payload.getall('option'),
    }
    try:
        vote = Vote.create(data)
    except:
        import traceback
        traceback.print_exc()
        api_error('Invalid data!', error_class=HTTPUnprocessableEntity)
    else:
        return vote.to_json()
