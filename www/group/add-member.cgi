#! /usr/bin/env python3

import group
import json
import sys

import cgi, cgitb
cgitb.enable()


def err(msg):
    return {"error": msg}


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
        json.dump(err("Missing RSS feed"), sys.stdout)
        return

    cursor, conn = group.connect()
    cursor.execute("INSERT INTO users (name, rss) VALUES (%s, %s) RETURNING id",
                   (name, rss))
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
