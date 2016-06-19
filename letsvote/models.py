#!/usr/bin/env python
# coding=utf-8
import sqlite3
from .db import cursor, commit

class AlreadyVoted(Exception): pass
class InvalidData(Exception): pass

class Option:
    checked = False

    def __init__(self, data):
        self.oid = data['id']
        self.title = data['title']
        self.total = data['total']

    def to_json(self):
        return {
            'id': self.oid,
            'title': self.title,
            'total': self.total,
        }

class Poll:
    uid = None
    voted = False

    def __init__(self, data):
        self.vid = data['id']
        self.title = data['title']
        self.desc = data['desc']
        self.vtype = data['vtype']
        self.uid = data['user_id']
        self.options = []

    def get_option(self, oid):
        return self.option_map.get(str(oid))

    def set_options(self, options):
        self.options = list(options)
        self.option_map = dict([(str(option.oid), option) for option in self.options])

    def to_json(self):
        return {
            'id': self.vid,
            'title': self.title,
            'desc': self.desc,
            'type': self.vtype,
            'options': [option.to_json() for option in self.options],
        }

    @staticmethod
    def load(vid, user_id = None):
        cur = cursor()
        cur.execute('SELECT * FROM poll_meta WHERE id=?', (vid,))
        data = cur.fetchone()
        if data is None: return
        data['user_id'] = user_id
        poll = Poll(data)
        cur.execute('SELECT * FROM poll_option WHERE poll_id=?', (vid,))
        poll.set_options(map(Option, cur))
        if user_id is not None:
            cur.execute('SELECT option_id FROM vote_meta INNER JOIN vote_data '
                    'ON vote_meta.id=vote_data.vote_id '
                    'WHERE poll_id=? AND user_id=?', (vid, user_id))
            for item in cur:
                option = poll.get_option(item['option_id'])
                option.checked = True
                poll.voted = True
        return poll

    @staticmethod
    def create(data):
        if len(data['options']) < 2:
            raise InvalidData('At least 2 options are required!')
        cur = cursor()
        cur.execute('INSERT INTO poll_meta (title,desc,created_by,vtype) VALUES (?,?,?,?)',
                (data['title'], data['desc'], data['user_id'], 1))
        data['vtype'] = 1
        data['id'] = cur.lastrowid
        poll = Poll(data)
        cur.executemany('INSERT INTO poll_option (poll_id,title) VALUES (?,?)',
                [(poll.vid, option) for option in data['options']])
        commit()
        return poll

    def vote(self, oids):
        cur = cursor()
        try:
            cur.execute('INSERT INTO vote_meta (poll_id,user_id) VALUES (?,?)', (self.vid, self.uid))
            vote_id = cur.lastrowid
        except sqlite3.IntegrityError:
            raise AlreadyVoted
        cur.executemany('INSERT INTO vote_data (vote_id,option_id) VALUES (?,?)',
                [(vote_id, oid) for oid in oids])
        cur.executemany('UPDATE poll_option SET total=total+1 WHERE id=?',
                [(oid,) for oid in oids])
        commit()
        for oid in oids:
            option = self.get_option(oid)
            option.total += 1
            option.checked = True
            self.voted = True

class User:
    def __init__(self, data):
        self.uid = data['id']
        self.oauth_id = data['oauth_id']
        self.update_data(data)

    def update_data(self, data):
        self.name = data['name']
        self.email = data['email']
        self.avatar_url = data['avatar_url']
        self.gravatar_id = data['gravatar_id']

    @staticmethod
    def create(data):
        cur = cursor()
        cur.execute('INSERT INTO user (oauth_id,name,email,avatar_url,gravatar_id,token) VALUES(?,?,?,?,?,?)',
                (data['oauth_id'], data['name'], data['email'], data['avatar_url'], data['gravatar_id'], data['token']))
        data['id'] = cur.lastrowid
        commit()
        return User(data)

    @staticmethod
    def load(id=None, oauth_id=None):
        if id is not None:
            key = 'id'
            args = id,
        elif oauth_id is not None:
            key = 'oauth_id'
            args = oauth_id,
        else:
            return
        cur = cursor()
        cur.execute('SELECT * FROM user WHERE %s=?' % key, args)
        data = cur.fetchone()
        if data is not None: return User(data)

    @staticmethod
    def update(data):
        user = User.load(oauth_id=data['oauth_id'])
        if user is None: return User.create(data)
        cur = cursor()
        cur.execute('UPDATE user SET name=?,email=?,avatar_url=?,gravatar_id=?,token=? WHERE id=?',
                (data['name'], data['email'], data['avatar_url'], data['gravatar_id'], data['token'], user.uid))
        commit()
        user.update_data(data)
        return user
