#! /usr/bin/env python3

import auth
import group.group
import http.cookies
import os
import urllib.parse

import cgi, cgitb
cgitb.enable()


def get_group_id(cursor, user_id):
    cursor.execute("SELECT group_id FROM group_users WHERE user_id = %s", (user_id,))
    row = cursor.fetchone()
    return row[0]


def wordpress_webhook_url(user_id, group_id, auth_string):
    return ("https://eric.willisson.org/rss-groups/wordpress-webhook.cgi?"
            + urllib.parse.urlencode({"id": group_id, "auth": auth_string}))


def page(user_id, auth_string):
    print("Content-Type: text/html\n")

    if not user_id:
        c = http.cookies.SimpleCookie(os.environ.get("HTTP_COOKIE"))
        user_id = c["user_id"].value
        auth_string = c["auth"].value
    
    cursor, conn = group.group.connect()
    user = group.group.get_user(user_id, cursor)
    if not auth.auth_user(user, auth_string):
        print("<html><body><h1>Not authenticated</h1></body></html>")
        return

    group_id = get_group_id(cursor, user_id)

    format_args = {"id": user.user_id,
                   "name": user.name,
                   "rss": user.rss,
                   "type": user.blog_type,
                   "auth": user.auth(),
                   "personal_rss": user.link(group_id),
                   "wordpress_webhook": wordpress_webhook_url(user_id, group_id, auth_string),
    }

    with open("blog.template.html") as f:
        print(f.read().format(**format_args))


def main():
    args = cgi.FieldStorage()
    page(args.getfirst("id"), args.getfirst("auth"))


if __name__ == "__main__":
    main()
