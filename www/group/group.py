#! /usr/bin/env python3

import psycopg2


class User(object):
    def __init__(self, user_id, name=None, rss=None, username=None, password=None):
        self.user_id = user_id
        self.name = name
        self.rss = rss
        self.username = username
        self.password = password

    def link_params(self, username, password, group_id):
        auth = ""
        if username and password:
            auth = username + ":" + password + "@"
        return "https://{}eric.willisson.org/rss-groups/rss-groups.cgi?id={}".format(auth, group_id)
        
    def link(self, group_id):
        return self.link_params(self.username, self.password, group_id)


class Group(object):
    def __init__(self, group_id=None, name=None):
        self.group_id = group_id
        self.name = name
        self.users = {}

    def add_user(self, user):
        self.users[user.user_id] = user


def connect():
    conn = psycopg2.connect("dbname=rssgroups user='www-data'")
    return conn.cursor(), conn

        
def get_group(group_id):
    cursor, _ = connect()
    cursor.execute("SELECT id, name FROM groups WHERE id = %s", (group_id,))
    row = cursor.fetchone()
    group = Group(row[0], row[1])
    cursor.execute("SELECT user_id FROM group_users WHERE group_id = %s", (group_id,))
    for row in cursor:
        group.add_user(User(row[0]))
    if len(group.users) > 0:
        user_choices = "id = " + " OR id = ".join([str(user) for user in group.users])
        cursor.execute("SELECT id, name, rss, username, password FROM users WHERE " + user_choices)
        for row in cursor:
            group.users[row[0]].name = row[1]
            group.users[row[0]].rss = row[2]
            group.users[row[0]].username = row[3]
            group.users[row[0]].password = row[4]
    return group
