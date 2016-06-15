#!/usr/bin/env python
# coding=utf-8
import sqlite3
from .db import cursor, commit

class AlreadyVoted(Exception): pass

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

class Vote:
    readonly = False
    uid = None

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
        cur.execute('SELECT * FROM vote_meta WHERE id=?', (vid,))
        data = cur.fetchone()
        if data is None: return
        data['user_id'] = user_id
        vote = Vote(data)
        cur.execute('SELECT * FROM vote_options WHERE vote_id=?', (vid,))
        vote.set_options(map(Option, cur))
        if user_id is not None:
            cur.execute('SELECT option_id FROM vote_user INNER JOIN vote_data '
                    'ON vote_user.id=vote_data.vote_user_id '
                    'WHERE vote_id=? AND user_id=?', (vid, user_id))
            for item in cur:
                option = vote.get_option(item['option_id'])
                option.checked = True
                vote.readonly = True
        return vote

    @staticmethod
    def create(data):
        cur = cursor()
        cur.execute('INSERT INTO vote_meta (title,desc,created_by,vtype) VALUES (?,?,?,?)',
                (data['title'], data['desc'], data['user_id'], 1))
        data['vtype'] = 1
        data['id'] = cur.lastrowid
        vote = Vote(data)
        cur.executemany('INSERT INTO vote_options (vote_id,title) VALUES (?,?)',
                [(vote.vid, option) for option in data['options']])
        commit()
        return vote

    def vote(self, oids):
        cur = cursor()
        try:
            cur.execute('INSERT INTO vote_user (vote_id,user_id) VALUES (?,?)', (self.vid, self.uid))
            vote_user_id = cur.lastrowid
        except sqlite3.IntegrityError:
            raise AlreadyVoted
        cur.executemany('INSERT INTO vote_data (vote_user_id,option_id) VALUES (?,?)',
                [(vote_user_id, oid) for oid in oids])
        cur.executemany('UPDATE vote_options SET total=total+1 WHERE id=?',
                [(oid,) for oid in oids])
        commit()
        for oid in oids:
            option = self.get_option(oid)
            option.total += 1
            option.checked = True
            self.readonly = True
