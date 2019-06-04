#! /usr/bin/env python3

import google.oauth2.credentials
import googleapiclient.discovery

#from oauth2client import client
#from googleapiclient import sample_tools
import json
import make_rss_item

import sys


def get_blog(cursor, user_id, url):
    cursor.execute("SELECT credentials, rss FROM users WHERE id = %s", (user_id,))
    row = cursor.fetchone()

    credentials = google.oauth2.credentials.Credentials(
        **json.loads(row[0]))

    blogger = googleapiclient.discovery.build(
        "blogger", "v3", credentials=credentials)
    return blogger, blogger.blogs().getByUrl(url=row[1]).execute()


# def get_blog(url):
#   # Authenticate and construct service.
#   service, flags = sample_tools.init(
#     ["blogger", "--noauth_local_webserver"], 'blogger', 'v3', __doc__, "/home/eric/projects/rss-groups/client_secrets.json",
#     scope='https://www.googleapis.com/auth/blogger')

#   blogs = service.blogs()

#   return blogs.getByUrl(url=url).execute()


  

def rss(cursor, user_id, url):
    # try:
    #     blogger, blog = get_blog(cursor, user_id, url)
    # except blogger.google.auth.exceptions.RefreshError:
    #     sys.stderr.write("Refresh error")
    #     raise
    blogger, blog = get_blog(cursor, user_id, url)
  
    posts = blogger.posts().list(blogId=blog["id"]).execute()

    items = []
    for post in posts["items"]:
        items.append(make_rss_item.make_item(
            title=post["title"],
            blog_name=blog["name"],
            author_name=post["author"]["displayName"],
            url=post["url"],
            content=post["content"],
            pubdate=post["published"]))

    return items

