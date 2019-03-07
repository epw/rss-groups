#! /usr/bin/env python3

import sys

from oauth2client import client
from googleapiclient import sample_tools
import PyRSS2Gen


def main(argv):
  # Authenticate and construct service.
  service, flags = sample_tools.init(
      argv, 'blogger', 'v3', __doc__, __file__,
      scope='https://www.googleapis.com/auth/blogger')

  try:

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
        items.append(PyRSS2Gen.RSSItem(
          title=post["title"],
          link=post["url"],
          description=post["content"],
#          guid=
          pubDate=post["published"]))

      rss = PyRSS2Gen.RSS2(
        title=blog["name"],
        link=blog["url"],
        description=blog["description"],
        lastBuildDate=blog["updated"],
        items=items)

      print(rss.to_xml())
      
  except client.AccessTokenRefreshError:
    print ('The credentials have been revoked or expired, please re-run'
      'the application to re-authorize')

if __name__ == '__main__':
  main(sys.argv)
  
