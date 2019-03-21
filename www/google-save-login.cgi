#! /usr/bin/env python3

import google.oauth2.credentials
import google_auth_oauthlib.flow

import auth
import group.group
import http.cookies
import json
import os

import cgi, cgitb
cgitb.enable()

CLIENT_SECRET = "/var/local/rss-groups/client_secret_blogger_interface.json"
#SCOPES = ["profile", "email", "https://www.googleapis.com/auth/blogger"]
SCOPES = [
    "https://www.googleapis.com/auth/blogger",
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/userinfo.profile",
    "openid"
]
SERVER = "https://eric.willisson.org"

#print("Content-Type: text/plain\n")


def server_url(path):
    if path[0] == "/":
        return SERVER + path
    return SERVER + os.environ.get("SCRIPT_NAME").rsplit("/", 1)[0] + "/" + path


def credentials_to_dict(credentials):
  return {'token': credentials.token,
          'refresh_token': credentials.refresh_token,
          'token_uri': credentials.token_uri,
          'client_id': credentials.client_id,
          'client_secret': credentials.client_secret,
          'scopes': credentials.scopes}


def page():
    c = http.cookies.SimpleCookie(os.environ.get("HTTP_COOKIE"))
    user_id = c["user_id"].value
    auth_string = c["auth"].value
    
    cursor, conn = group.group.connect()
    user = group.group.get_user(user_id, cursor)
    if not auth.auth_user(user, auth_string):
        print("Content-Type: text/plain\n")
        print("Not authenticated")
        return

    cursor.execute("SELECT state FROM users WHERE id = %s", (user_id,))
    row = cursor.fetchone()
    state = row[0]
    
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CLIENT_SECRET, scopes=SCOPES, state=state)
    flow.redirect_uri = server_url("google-save-login.cgi")
    flow.fetch_token(authorization_response=server_url(os.environ.get("REQUEST_URI")))

    print("Content-Type: text/plain")
    print("Location: " + server_url("blog.cgi"))
    print()

    credentials = credentials_to_dict(flow.credentials)
    cursor.execute("UPDATE users SET credentials = %s WHERE id = %s", (json.dumps(credentials), user_id))
    conn.commit()



def main():
    args = cgi.FieldStorage()
    page()


if __name__ == "__main__":
    main()
