#! /usr/bin/env python3


class unprintable(object):
    pass

NOT_AUTHENTICATED = unprintable()


def auth(rssgroup, auth_string):
    if auth_string:
        username, password = auth_string.split(":")
    else:
        return False
    entries = []
    for user in rssgroup.users:
        if username == rssgroup.users[user].username and password == rssgroup.users[user].password:
            return rssgroup.users[user]
    return False

def auth_user(user, auth_string):
    if auth_string:
        username, password = auth_string.split(":")
    else:
        return False
    return username == user.username and password == user.password
