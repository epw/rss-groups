#! /usr/bin/env python3

import group

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
    print("Content-Type: text/html\n")

    args = cgi.FieldStorage()

    group_id = args.getfirst("id")
    if not group_id:
        print("<html><body>id= parameter needed</body></html>")
        return
    
    format_args = {"members": member_table(int(group_id))}

    with open("index.template.html") as f:
        print(f.read().format(**format_args))


def main():
    page()


if __name__ == "__main__":
    main()
