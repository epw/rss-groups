#! /usr/bin/env python3

import auth
import feedparser
import rss_io
import blogger
import group.group
import os

import cgi, cgitb


def add_source(entry, parsed):
    if "title" in dir(parsed.feed):
        entry.publisher = parsed.feed.title
    return entry


def get_entries(users, cursor):
    entries = []
    rssentries = []
    for user in users:
        if users[user].blog_type == 'wordpress':
            cursor.execute("SELECT xml FROM posts WHERE user_id = %s", (users[user].user_id,))
            for row in cursor:
                parsed = feedparser.parse(row[0])
                entries.append(add_source(parsed.entries[0], parsed))
        elif users[user].blog_type == 'blogger':
            try:
                rssentries = blogger.rss(users[user].rss)
            except blogger.client.AccessTokenRefreshError:
                print ('<?xml version="1.0"><error>The credentials have been revoked or expired, please re-run'
                       'the application to re-authorize</error>')
                exit()
        else:
            parsed = feedparser.parse(users[user].rss)
            entries.extend([add_source(entry, parsed) for entry in parsed.entries])
    return entries, rssentries


def rss_groups(group_id, auth_string):
    print("Content-Type: text/xml; charset=utf-8\n")

    cursor, conn = group.group.connect()
    rssgroup = group.group.get_group(group_id, cursor)
    if not auth.auth(rssgroup, auth_string):
        print("<?xml version='1.0'?>")
        print("<error>Not authenticated</error>")
        return

    entries, rssentries = get_entries(rssgroup.users, cursor)

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
    cgitb.enable()
    args = cgi.FieldStorage()
    rss_groups(args.getfirst("id"), args.getfirst("auth"))


if __name__ == "__main__":
    main()
