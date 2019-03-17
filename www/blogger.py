#! /usr/bin/env python3

from oauth2client import client
from googleapiclient import sample_tools
import make_rss_item


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
    items.append(make_rss_item.make_item(
      title=post["title"],
      blog_name=blog["name"],
      author_name=post["author"]["displayName"],
      url=post["url"],
      content=post["content"],
      pubDate=post["published"]))

  return items

