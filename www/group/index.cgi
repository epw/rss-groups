#! /usr/bin/env python3

import group

import cgi, cgitb
cgitb.enable()


def member_table(users):
    table = ["<table class='members' border='1'>",
             "<tr><th>Name</th><th>RSS Feed</th></tr>"]
    for user in sorted(users.keys()):
            table.append("<tr><td>{}</td><td>{}</td></tr>".format(users[user].name, users[user].rss))
    table.append("</table>")
    return "\n".join(table)


def page():
    print("Content-Type: text/html\n")

    args = cgi.FieldStorage()

    group_id = args.getfirst("id")
    if not group_id:
        with open("new.template.html") as f:
            print(f.read().format())
            return

    rssgroup = group.get_group(int(group_id))
    format_args = {"name": rssgroup.name, "members": member_table(rssgroup.users)}

    with open("index.template.html") as f:
        print(f.read().format(**format_args))


def main():
    page()


if __name__ == "__main__":
    main()
