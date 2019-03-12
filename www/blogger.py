#! /usr/bin/env python3

from oauth2client import client
from googleapiclient import sample_tools
import PyRSS2Gen as RSS2
import datetime
import dateparser
import pytz


def rss():
  # Authenticate and construct service.
  service, flags = sample_tools.init(
    ["blogger", "--noauth_local_webserver"], 'blogger', 'v3', __doc__, "/home/eric/projects/rss-groups/client_secrets.json",
    scope='https://www.googleapis.com/auth/blogger')

  blogs = service.blogs()

#      blog = blogs.getByUrl(url="https://ericpublicblog.blogspot.com").execute()
  blog = blogs.getByUrl(url="https://ericrssexperiments.blogspot.com").execute()

#      code.interact(local={"client": client, "sample_tools": sample_tools,
#                           "service": service, "users": users, "thisuser": thisuser,
#                           "blogs": blogs, "thisusersblogs": thisusersblogs})
#      exit()

  posts = service.posts().list(blogId=blog["id"]).execute()

  items = []
  for post in posts["items"]:
    items.append(RSS2.RSSItem(
      title=post["title"],
      author=blog["name"] + " - " + post["author"]["displayName"],
      link=post["url"],
      description=post["content"],
      guid=post["url"],
      pubDate=dateparser.parse(post["published"]).replace(tzinfo=pytz.utc)))

  return items

