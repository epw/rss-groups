#! /usr/bin/env python3

from oauth2client import client
from googleapiclient import sample_tools
import PyRSS2Gen as RSS2
import datetime
import dateparser
import pytz

import locale

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
      author=post["author"]["displayName"],
      link=post["url"],
      description=post["content"],
      guid=post["url"],
      pubDate=dateparser.parse(post["published"]).replace(tzinfo=pytz.utc)))

  items.append(RSS2.RSSItem(
    title="Information",
    author="The System",
    link="http://example.com",
    description="The value of the preferred encoding is " + locale.getpreferredencoding(),
    guid="http://example.com",
    pubDate=datetime.datetime.now().replace(tzinfo=pytz.utc)))
  return items

