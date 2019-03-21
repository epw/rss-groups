#! /usr/bin/env python3

import google.oauth2.credentials
import google_auth_oauthlib.flow

import auth
import group.group
import http.cookies

import cgi, cgitb

CLIENT_SECRET = "/var/local/rss-groups/client_secret_blogger_interface.json"


def not_authorized():
    print("""Content-Type: text/plain\n

<html><body><h1>Not authorized</h1></body></html>""")


def login(user_id, auth_string, token, url):
    cursor, conn = group.group.connect()
    user = group.group.get_user(user_id, cursor)
    if not auth.auth_user(user, auth_string):
        not_authorized()
        return

    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CLIENT_SECRET,
        scopes = ["https://www.googleapis.com/auth/blogger"])
    flow.redirect_uri = "https://eric.willisson.org/rss-groups/blog.cgi"

    authorization_url, state = flow.authorization_url(
        access_type="offline",
        include_granted_scopes="true")
    print("Content-Type: text/plain")
    print("Location: " + authorization_url)

    c = http.cookies.SimpleCookie()
    c["user_id"] = user_id
    c["auth"] = auth_string
    print(c)

    print()
    

def main():
    args = cgi.FieldStorage(encoding="UTF-8")
    login(args.getfirst("id"),
          args.getfirst("auth"),
          args.getfirst("idtoken"),
          args.getfirst("url"))


if __name__ == "__main__":
    main()
