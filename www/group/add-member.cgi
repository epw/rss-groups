#! /usr/bin/env python3

import base64
import group
import json
import os
import sys

import cgi, cgitb
cgitb.enable()


def err(msg):
    return {"error": msg}


def make_auth(name):
    username = base64.urlsafe_b64encode(bytes(name, "ascii")).decode("ascii")
    password = base64.urlsafe_b64encode(os.urandom(40)).decode("ascii")
    return username.replace("=", ""), password.replace("=", "")


def page():
    print("Content-Type: application/json\n")

    args = cgi.FieldStorage()

    group_id = args.getfirst("group_id")
    if not group_id:
        json.dump(err("Missing group ID"), sys.stdout)
        return
    name = args.getfirst("name")
    if not name:
        json.dump(err("No name given"), sys.stdout)
        return
    rss = args.getfirst("rss")
    if not rss:
        rss = ""
#        json.dump(err("Missing RSS feed"), sys.stdout)
#        return
    blog_type = args.getfirst("type")
    if not blog_type:
        blog_type = "rss"

    cursor, conn = group.connect()
    username, password = make_auth(name)
    cursor.execute("INSERT INTO users (name, rss, type, username, password) VALUES (%s, %s, %s, %s, %s) RETURNING id",
                   (name, rss, blog_type, username, password))
    conn.commit()
    user_id = cursor.fetchone()[0]

    cursor.execute("INSERT INTO group_users (group_id, user_id) VALUES (%s, %s)",
                   (group_id, user_id))
    conn.commit()

    json.dump({"success": user_id}, sys.stdout)
    

def main():
    page()


if __name__ == "__main__":
    main()
