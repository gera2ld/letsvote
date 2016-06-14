#!/usr/bin/env python
# coding=utf-8
import sqlite3
__all__ = ['cursor', 'commit']

def dict_factory(cursor, row):
    res = {}
    for i, col in enumerate(cursor.description):
        res[col[0]] = row[i]
    return res

db = sqlite3.connect('data.sqlite')
db.row_factory = dict_factory

cursor = db.cursor
commit = db.commit
