#! /usr/bin/env python3

import group

import cgi, cgitb
cgitb.enable()


def name_link(user):
    return "<a href='../blog.cgi?id={id}&auth={auth}'>{name}</a>".format(
        id=user.user_id,
        auth=user.auth(),
        name=user.name)


def member_table(users, group_id):
    table = ["<table class='members' border='1'>",
             "<tr><th>Name</th><th>RSS Feed</th><th>Type</th><th>Group URL</th></tr>"]
    for user in sorted(users.keys()):
            table.append("<tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>".format(
                name_link(users[user]),
                users[user].rss,
                users[user].blog_type,
                users[user].link(group_id)))
    table.append("</table>")
    return "\n".join(table)


def checked_if(value):
    if value:
        return "checked"
    return ""


def page():
    print("Content-Type: text/html\n")

    args = cgi.FieldStorage()

    group_id = args.getfirst("id")
    if not group_id:
        with open("new.template.html") as f:
            print(f.read().format())
            return

    rssgroup = group.get_group(int(group_id))
    format_args = {"name": rssgroup.name,
                   "members": member_table(rssgroup.users, group_id),
                   "public": checked_if(rssgroup.public),
                   "public_url": group.url_base(group_id)
    }

    with open("index.template.html") as f:
        print(f.read().format(**format_args))


def main():
    page()


if __name__ == "__main__":
    main()
