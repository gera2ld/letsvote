#!/usr/bin/env python
# coding=utf-8
import json
import aiohttp_jinja2, aiohttp
from aiohttp_session import get_session
from .models import *
from . import callbacks

async def get_user(request):
    session = await get_session(request)
    user_id = session.get('user_id')
    user_name = session.get('user_name')
    return user_id, user_name

def safe_get_poll(vid, user_id):
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
    poll = safe_get_poll(request.match_info['vid'], user_id)
    return {
        'poll': poll,
        'user_name': user_name,
    }

@render('detail.html')
async def handle_post_detail(request):
    user_id, user_name = await get_user(request)
    poll = safe_get_poll(request.match_info['vid'], user_id)
    data = await request.post()
    oids = data.getall('voteGroup')
    data = {
        'poll': poll,
        'user_name': user_name,
    }
    if user_id is None:
        data['message'] = 'Please log in first!'
    else:
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
    except InvalidData as e:
        args = e.args
        message = args[0] if len(args) > 0 else 'Invalid data!'
        data['message'] = message
    except:
        import traceback
        traceback.print_exc()
        data['message'] = 'Unknown error!'
    else:
        raise aiohttp.web.HTTPFound('/polls/' + str(poll.vid))
    data['json_options'] = json.dumps(data['options'])
    return data

async def handle_callback(request):
    try:
        user = await callbacks.handle(request)
    except:
        pass
    session = await get_session(request)
    if user is None:
        session['user_id'] = session['user_name'] = None
    else:
        session['user_id'] = user.uid
        session['user_name'] = user.name
    raise aiohttp.web.HTTPFound('/')
