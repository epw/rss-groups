#! /usr/bin/env python3

import group
import json
import sys

import cgi, cgitb
cgitb.enable()


def member_table(group_id):
    rssgroup = group.get_group(group_id)
    table = ["<table class='members' border='1'>",
             "<tr><th>Name</th><th>RSS Feed</th></tr>"]
    for user in sorted(rssgroup.users.keys()):
            table.append("<tr><td>{}</td><td>{}</td></tr>".format(rssgroup.users[user].name, rssgroup.users[user].rss))
    table.append("</table>")
    return "\n".join(table)


def page():
    print("Content-Type: application/json\n")

    args = cgi.FieldStorage()

    rssgroup = group.get_group(args.getfirst("id", 1))

    response = {
        "id": rssgroup.group_id,
        "name": rssgroup.name,
        "members": []
    }
    for user in rssgroup.users:
        member = rssgroup.users[user]
        response["members"].append({
            "id": member.user_id,
            "name": member.name,
            "rss": member.rss
        })
    json.dump(response, sys.stdout)
    

def main():
    page()


if __name__ == "__main__":
    main()
