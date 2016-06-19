#!/usr/bin/env python
# coding=utf-8
import json
import aiohttp_jinja2, aiohttp
from aiohttp_session import get_session
from .models import *

async def get_user(request):
    session = await get_session(request)
    user_id = session.get('user_id')
    user_name = session.get('user_name')
    return user_id, user_name

async def safe_get_poll(vid, user_id):
    poll = Poll.load(vid, user_id)
    if poll is None:
        raise aiohttp.web.HTTPFound('/')
    return poll

def render(template):
    def wrapper(handle):
        async def wrapped(request):
            data = await handle(request)
            data['login'] = request.app.config.login
            return aiohttp_jinja2.render_template(template, request, data)
        return wrapped
    return wrapper

@render('detail.html')
async def handle_get_detail(request):
    user_id, user_name = await get_user(request)
    poll = await safe_get_poll(request.match_info['vid'], user_id)
    return {
        'poll': poll,
        'user_name': user_name,
    }

@render('detail.html')
async def handle_post_detail(request):
    user_id, user_name = await get_user(request)
    poll = await safe_get_poll(request.match_info['vid'], user_id)
    data = await request.post()
    oids = data.getall('voteGroup')
    data = {
        'poll': poll,
        'user_name': user_name,
    }
    try:
        poll.vote(oids)
    except AlreadyVoted:
        data['message'] = 'You have already voted!'
    return data

@render('create.html')
async def handle_get_create(request):
    _, user_name = await get_user(request)
    return {
        'user_name': user_name
    }

@render('create.html')
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
        data['json_options'] = json.dumps(data['options'])
        return data
    else:
        raise aiohttp.web.HTTPFound('/polls/' + str(poll.vid))
