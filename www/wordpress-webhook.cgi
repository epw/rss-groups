#! /usr/bin/env python3

import auth
import group.group
import make_rss_item
import sys

import cgi, cgitb
cgitb.enable()


def webhook():
    print("Content-Type: text/plain\n")

    args = cgi.FieldStorage()
    
    cursor, conn = group.group.connect()
    group_id = args.getfirst("id")
    rssgroup = group.group.get_group(group_id, cursor)
    user = auth.auth(rssgroup, args.getfirst("auth"))
    if not user:
        print("ERROR: Not authenticated")
        return

    cursor.execute("SELECT name FROM users WHERE id=%s", (user.user_id,))
    row = cursor.fetchone()
    item = make_rss_item.make_item(
        title=args.getfirst("post_title"),
        blog_name=row[0],
        author_name=None, # Haven't been able to figure out how to retrieve Wordpress user
        url=args.getfirst("post_url"),
        content=args.getfirst("post_content"),
        pubdate=args.getfirst("post_date"))

    cursor.execute("SELECT id FROM posts WHERE url=%s", (item.link,))
    row = cursor.fetchone()
    if row:
        cursor.execute("UPDATE posts SET xml = %s WHERE id = %s", (item.to_xml(), row[0]))
    else:
        cursor.execute("INSERT INTO posts (user_id, type, url, xml) VALUES ("
                       "%s, 'wordpress', %s, %s)",
                       (user.user_id, args.getfirst("post_url"), item.to_xml()))
    conn.commit()
    
    print("OK")


def main():
    webhook()


if __name__ == "__main__":
    main()
