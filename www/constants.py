#! /usr/bin/env python3

CLIENT_SECRET = "/var/local/rss-groups/client_secret_blogger_interface.json"
#SCOPES = ["profile", "email", "https://www.googleapis.com/auth/blogger"]
SCOPES = [
    "https://www.googleapis.com/auth/blogger.readonly",
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/userinfo.profile",
    "openid"
]
SERVER = "https://eric.willisson.org"
