#! /usr/bin/env python3

import feedparser
import rss_io
import blogger
import group.group
import login
import os

import cgi, cgitb
cgitb.enable()


def add_source(entry, parsed):
    entry.publisher = parsed.feed.title
    return entry


class unprintable(object):
    pass

NOT_AUTHENTICATED = unprintable()


def rss_groups():
    args = cgi.FieldStorage()

    print("Content-Type: text/xml; charset=utf-8\n")

    group_id = args.getfirst("id", 4)
    auth = args.getfirst("auth")
    if auth:
        username, password = auth.split(":")
    else:
        username = NOT_AUTHENTICATED
        password = NOT_AUTHENTICATED
    rssgroup = group.group.get_group(group_id)
    entries = []
    authenticated = False
    for user in rssgroup.users:
        if username == rssgroup.users[user].username and password == rssgroup.users[user].password:
            authenticated = True
#    if username == "1" and password == "1":
    authenticated = True
    if not authenticated:
        print("<?xml version='1.0'?>")
        print("<error>Not authenticated</error>")
        return
        
    for user in rssgroup.users:
        if rssgroup.users[user].blog_type == 'wordpress':
            rss = login.wordpress(rssgroup.users[user].rss)
#        parsed = feedparser.parse(rssgroup.users[user].rss)
        parsed = feedparser.parse(rss)
        entries.extend([add_source(entry, parsed) for entry in parsed.entries])

#    try:
#        rssentries = blogger.rss()
#    except blogger.client.AccessTokenRefreshError:
#        print ('<?xml version="1.0"><error>The credentials have been revoked or expired, please re-run'
#               'the application to re-authorize</error>')
#        exit()
    rssentries = []
    xml = rss_io.feedparser_to_rss2(rssgroup.name,
                                    "https://eric.willisson.org/rss-groups/rss-groups.cgi?id={}".format(group_id),
                                    "First try at a combined feed",
                                    entries, rssentries)

    # If you're getting weird UnicodeDecode errors, then use this temporarily.
    # You'll have to edit the server to change the environment variables to LANG=en_US.UTF-8
    #    print(xml.encode("ascii", "namereplace").decode("ascii", "namereplace"))

    print(xml.split("\n")[0])
    print("<?xml-stylesheet type='text/css' href='style.css' ?>")
    print(xml.split("\n", 1)[1])


def main():
    rss_groups()


if __name__ == "__main__":
    main()
