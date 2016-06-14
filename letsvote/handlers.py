#!/usr/bin/env python
# coding=utf-8
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
async def handle_get(request):
    vote = get_vote(request)
    return {
        'vote': vote
    }

@render('detail.html')
async def handle_post(request):
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
