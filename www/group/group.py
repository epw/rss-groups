#! /usr/bin/env python3

import psycopg2


class User(object):
    def __init__(self, user_id, name=None, rss=None):
        self.user_id = user_id
        self.name = name
        self.rss = rss


class Group(object):
    def __init__(self, group_id=None, name=None):
        self.group_id = group_id
        self.name = name
        self.users = {}

    def add_user(self, user):
        self.users[user.user_id] = user


def get_group(group_id):
    conn = psycopg2.connect("dbname=rssgroups user='www-data'")
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM groups WHERE id = %s", (group_id,))
    row = cursor.fetchone()
    group = Group(row[0], row[1])
    cursor.execute("SELECT user_id FROM group_users WHERE group_id = %s", (group_id,))
    for row in cursor:
        group.add_user(User(row[0]))
    if len(group.users) > 0:
        user_choices = "id = " + " OR id = ".join([str(user) for user in group.users])
        cursor.execute("SELECT id, name, rss FROM users WHERE " + user_choices)
        for row in cursor:
            group.users[row[0]].name = row[1]
            group.users[row[0]].rss = row[2]
    return group
