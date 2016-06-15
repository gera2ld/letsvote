#!/usr/bin/env python
# coding=utf-8
from .models import Vote

def user_id(request):
    peer = request.transport.get_extra_info('peername')
    ip, port = peer[:2]
    return ip

def get_vote(request):
    vid = request.match_info['vid']
    vote = Vote.load(vid, user_id(request))
    return vote
