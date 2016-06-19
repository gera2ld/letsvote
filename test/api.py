#!/usr/bin/env python
# coding=utf-8
import aiohttp

prefix = 'http://localhost:3002/api'

async def test_post_create(session):
    async with session.post(prefix + '/polls', data = {
        'title': 'test_title_1',
        'desc': 'test_desc_1',
        'option': [
            'test_option_1',
            'test_option_2',
            'test_option_3',
        ],
    }) as res:
        data = await res.json()
        print(data)
        return data

async def test_get_detail(session, voting):
    async with session.get(prefix + '/polls/' + str(voting['id'])) as res:
        data = await res.json()
        print(data)
        return data

async def test_post_detail(session, voting):
    votes = {
        'voteGroup': [voting['options'][0]['id']],
    }
    async with session.post(prefix + '/polls/' + str(voting['id']), data=votes) as res:
        data = await res.json()
        print(data)
        return data

async def test():
    async with aiohttp.ClientSession() as session:
        voting_meta = await test_post_create(session)
        voting = await test_get_detail(session, voting_meta)
        voting = await test_post_detail(session, voting)
