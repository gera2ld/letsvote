#!/usr/bin/env python
# coding=utf-8
import sys
sys.path.insert(0, '')
from letsvote import db

cur = db.cursor()
cur.executescript('''
DROP TABLE IF EXISTS vote_meta;
DROP TABLE IF EXISTS vote_options;
DROP TABLE IF EXISTS vote_user;
DROP TABLE IF EXISTS vote_data;
''')
cur.executescript('''
CREATE TABLE IF NOT EXISTS vote_meta (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR,
    desc VARCHAR,
    created_by VARCHAR,
    vtype INTEGER DEFAULT 1
);
CREATE TABLE IF NOT EXISTS vote_options (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    vote_id INTEGER,
    title VARCHAR,
    total INTEGER DEFAULT 0
);
CREATE TABLE IF NOT EXISTS vote_user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    vote_id INTEGER,
    user_id VARCHAR
);
CREATE TABLE IF NOT EXISTS vote_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    vote_user_id INTEGER,
    option_id INTEGER
);
CREATE UNIQUE INDEX IF NOT EXISTS uniuser ON vote_user(vote_id, user_id);
CREATE UNIQUE INDEX IF NOT EXISTS unidata ON vote_data(vote_user_id, option_id);
''')
db.commit()

def mock():
    cur.execute('INSERT INTO vote_meta (title, desc) VALUES (?, ?)', ('Hello', 'Hello world'))
    mid = cur.lastrowid
    for title in [
        '一',
        '二',
        '三',
    ]:
        cur.execute('INSERT INTO vote_options (vote_id, title) VALUES (?, ?)', (mid, title))
    db.commit()

mock()
