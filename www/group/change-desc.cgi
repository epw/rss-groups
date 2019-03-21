#! /usr/bin/env python3

import group
import json
import os
import sys

import cgi, cgitb
cgitb.enable()


def err(msg):
    return {"error": msg}


def page(group_id, description):
    print("Content-Type: application/json\n")

    if not group_id:
        json.dump(err("Missing group ID"), sys.stdout)
        return

    cursor, conn = group.connect()
    cursor.execute("UPDATE groups SET description = %s WHERE id = %s", (description, group_id))
    conn.commit()

    json.dump({"success": group_id, "description": description}, sys.stdout)
    

def main():
    args = cgi.FieldStorage()
    page(args.getfirst("group_id"), args.getfirst("description"))


if __name__ == "__main__":
    main()
