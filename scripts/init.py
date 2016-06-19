#!/usr/bin/env python
# coding=utf-8
import sys
sys.path.insert(0, '')
from letsvote import db

cur = db.cursor()
cur.executescript('''
DROP TABLE IF EXISTS poll_meta;
DROP TABLE IF EXISTS poll_options;
DROP TABLE IF EXISTS vote_meta;
DROP TABLE IF EXISTS vote_data;
DROP TABLE IF EXISTS user;
''')
cur.executescript('''
CREATE TABLE IF NOT EXISTS poll_meta (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR,
    desc VARCHAR,
    created_by VARCHAR,
    vtype INTEGER DEFAULT 1
);
CREATE TABLE IF NOT EXISTS poll_option (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    poll_id INTEGER,
    title VARCHAR,
    total INTEGER DEFAULT 0
);
CREATE TABLE IF NOT EXISTS vote_meta (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    poll_id INTEGER,
    user_id VARCHAR
);
CREATE UNIQUE INDEX IF NOT EXISTS uniuser ON vote_meta(poll_id, user_id);
CREATE TABLE IF NOT EXISTS vote_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    vote_id INTEGER,
    option_id INTEGER
);
CREATE UNIQUE INDEX IF NOT EXISTS unidata ON vote_data(vote_id, option_id);
CREATE TABLE IF NOT EXISTS user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    oauth_id VARCHAR,
    name VARCHAR,
    email VARCHAR,
    avatar_url VARCHAR,
    gravatar_id VARCHAR,
    token VARCHAR
);
CREATE INDEX IF NOT EXISTS idx_oauth_id ON user(oauth_id);
''')
db.commit()

def mock():
    cur.execute('INSERT INTO poll_meta (title, desc) VALUES (?, ?)', ('Hello', 'Hello world'))
    mid = cur.lastrowid
    for title in [
        '一',
        '二',
        '三',
    ]:
        cur.execute('INSERT INTO poll_option (poll_id, title) VALUES (?, ?)', (mid, title))
    db.commit()

#mock()
