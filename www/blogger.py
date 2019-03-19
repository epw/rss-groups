#! /usr/bin/env python3

from oauth2client import client
from googleapiclient import sample_tools
import make_rss_item


def get_blog(url):
  # Authenticate and construct service.
  service, flags = sample_tools.init(
    ["blogger", "--noauth_local_webserver"], 'blogger', 'v3', __doc__, "/home/eric/projects/rss-groups/client_secrets.json",
    scope='https://www.googleapis.com/auth/blogger')

  blogs = service.blogs()

  return blogs.getByUrl(url=url).execute()
  

def rss(url):
  blog = get_blog(url)
  
  posts = service.posts().list(blogId=blog["id"]).execute()

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

