#! /usr/bin/env python3

import group
import json
import os
import sys

import cgi, cgitb
cgitb.enable()


def err(msg):
    return {"error": msg}


def arg_to_bool(arg):
    if not arg or arg == "0" or arg.lower() == "false":
        return False
    return True


def page(group_id, public):
    print("Content-Type: application/json\n")

    if not group_id:
        json.dump(err("Missing group ID"), sys.stdout)
        return

    cursor, conn = group.connect()
    cursor.execute("UPDATE groups SET public = %s WHERE id = %s", (public, group_id))
    conn.commit()

    json.dump({"success": group_id, "public": public}, sys.stdout)
    

def main():
    args = cgi.FieldStorage()
    page(args.getfirst("group_id"), arg_to_bool(args.getfirst("public")))


if __name__ == "__main__":
    main()
