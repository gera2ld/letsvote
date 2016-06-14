#!/usr/bin/env python
# coding=utf-8
import json
import aiohttp_jinja2, aiohttp
from .models import *

def user_id(request):
    peer = request.transport.get_extra_info('peername')
    ip, port = peer[:2]
    return ip

def get_vote(request):
    vid = request.match_info['vid']
    vote = Vote.load(vid, user_id(request))
    if vote is None:
        raise aiohttp.web.HTTPFound('/')
    return vote

def render(template):
    def wrapper(handle):
        async def wrapped(request):
            data = await handle(request)
            return aiohttp_jinja2.render_template(template, request, data)
        return wrapped
    return wrapper

@render('detail.html')
async def handle_get_detail(request):
    vote = get_vote(request)
    return {
        'vote': vote
    }

@render('detail.html')
async def handle_post_detail(request):
    vote = get_vote(request)
    data = await request.post()
    oids = data.getall('voteGroup')
    data = {
        'vote': vote
    }
    try:
        vote.vote(oids)
    except AlreadyVoted:
        data['message'] = 'You have already voted!'
    return data

@render('create.html')
async def handle_get_create(request):
    return {
        'user_id': user_id(request)
    }

@render('create.html')
async def handle_post_create(request):
    data = await request.post()
    return {
        'title': data['title'],
        'desc': data['desc'],
        'json_options': json.dumps(data.getall('option')),
    }
    raise aiohttp.web.HTTPFound()
