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

    name = args.getfirst("name")
    if not name:
        json.dump(err("No name given"), sys.stdout)
        return

    cursor, conn = group.connect()
    cursor.execute("INSERT INTO groups (name) VALUES (%s) RETURNING id",
                   (name,))
    conn.commit()
    group_id = cursor.fetchone()[0]

    json.dump({"success": group_id}, sys.stdout)
    

def main():
    page()


if __name__ == "__main__":
    main()
