#! /usr/bin/env python3

from google.oauth2 import id_token
from google.auth.transport import requests as googlerequests
#import google.oauth2.credentials
#import google_auth_oauthlib.flow

import auth
import group.group
import requests

import cgi, cgitb

print("Content-Type: text/plain\n")


#CLIENT_ID = "145363362327-tsvcsck1stldh89po1b1n68haehccc5h.apps.googleusercontent.com"
CLIENT_ID = "145363362327-278kuv0n610968i9gi7m3tkhq8usjpg8.apps.googleusercontent.com"

#def get_blog_title(url, token):
#    blog = blogger.get_blog(url)
#    return blog["name"]
    #    r = requests.get("https://www.googleapis.com/blogger/v3/blogs/byurl?url={url}&key={token}".format(
#        url=url,
#        token=token))
#    return r.text


def login(user_id, auth_string, token, url):
    print("login()")
    cursor, conn = group.group.connect()
    user = group.group.get_user(user_id, cursor)
    print("Checking authentication")
    if not auth.auth_user(user, auth_string):
        print("Not authenticated")
        return

    try:
        print("Getting idinfo")
        # Specify the CLIENT_ID of the app that accesses the backend:
        idinfo = id_token.verify_oauth2_token(token, googlerequests.Request(), CLIENT_ID)

        print("Checking idinfo['iss']")
        if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
            raise ValueError('Wrong issuer.')

        print("Getting result")
        # ID token is valid. Get the user's Google Account ID from the decoded token.
        userid = idinfo['sub']
#        print(get_blog_title(url, token))
        print(str(idinfo))
    except ValueError:
        # Invalid token
        print ("Invalid Token")


def main():
    args = cgi.FieldStorage(encoding="UTF-8")
    login(args.getfirst("id"),
          args.getfirst("auth"),
          args.getfirst("idtoken"),
          args.getfirst("url"))


if __name__ == "__main__":
    main()
