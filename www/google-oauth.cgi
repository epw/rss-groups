#! /usr/bin/env python3

import google.oauth2.credentials
import google_auth_oauthlib.flow

import auth
import constants
import group.group
import http.cookies

import cgi, cgitb


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
        constants.CLIENT_SECRET,
        scopes = constants.SCOPES)
    flow.redirect_uri = "https://eric.willisson.org/rss-groups/google-save-login.cgi"

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

    cursor.execute("UPDATE users SET state = %s WHERE id = %s", (state, user_id))
    conn.commit()


def main():
    args = cgi.FieldStorage(encoding="UTF-8")
    login(args.getfirst("id"),
          args.getfirst("auth"),
          args.getfirst("idtoken"),
          args.getfirst("url"))


if __name__ == "__main__":
    main()
