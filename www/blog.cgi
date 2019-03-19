#! /usr/bin/env python3

import auth
import group.group
import os

import cgi, cgitb
cgitb.enable()


def page(user_id, auth_string):
    print("Content-Type: text/html\n")

    cursor, conn = group.group.connect()
    user = group.group.get_user(user_id, cursor)
    if not auth.auth_user(user, auth_string):
        print("<html><body><h1>Not authenticated</h1></body></html>")
        return

    format_args = {"id": user.user_id,
                   "name": user.name,
                   "rss": user.rss,
                   "type": user.blog_type,
                   "auth": auth.auth_string(user)}

    with open("blog.template.html") as f:
        print(f.read().format(**format_args))

def main():
    args = cgi.FieldStorage()
    page(args.getfirst("id"), args.getfirst("auth"))


if __name__ == "__main__":
    main()
