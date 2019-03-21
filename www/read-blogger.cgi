#! /usr/bin/env python3

import google.oauth2.credentials
import googleapiclient.discovery

import auth
import group.group
import http.cookies
import json
import os

import cgi, cgitb
cgitb.enable()


def page(user_id, auth_string):
    print("Content-Type: text/plain\n")

    if not user_id:
        c = http.cookies.SimpleCookie(os.environ.get("HTTP_COOKIE"))
        user_id = c["user_id"].value
        auth_string = c["auth"].value
    
    cursor, conn = group.group.connect()
    user = group.group.get_user(user_id, cursor)
    if not auth.auth_user(user, auth_string):
        print("<html><body><h1>Not authenticated</h1></body></html>")
        return

    cursor.execute("SELECT credentials, rss FROM users WHERE id = %s", (user_id,))
    row = cursor.fetchone()

    credentials = google.oauth2.credentials.Credentials(
        **json.loads(row[0]))

    blogger = googleapiclient.discovery.build(
        "blogger", "v3", credentials=credentials)

    print(dir(blogger))
    print()

    blog = blogger.blogs().getByUrl(url=row[1]).execute()
    print(blog["id"])

    posts = blogger.posts().list(blogId=blog["id"]).execute()
    print(posts)

  # items = []
  # for post in posts["items"]:
  #   items.append(make_rss_item.make_item(
  #     title=post["title"],
  #     blog_name=blog["name"],
  #     author_name=post["author"]["displayName"],
  #     url=post["url"],
  #     content=post["content"],
  #     pubdate=post["published"]))

  # return items

    

#    drive = googleapiclient.discovery.build(
#        "drive", "v2", credentials=credentials)

#    files = drive.files().list().execute()

#    print("Files:")
#    print(files)


def main():
    args = cgi.FieldStorage()
    page(args.getfirst("id"), args.getfirst("auth"))


if __name__ == "__main__":
    main()
