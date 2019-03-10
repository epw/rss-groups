#! /usr/bin/env python3

import sqlite3
import feedparser

import cgi, cgitb
cgitb.enable()


DATABASE = "/var/www/db/rss.sqlite"


def rss_groups():
    args = cgi.FieldStorage()

    print "Content-Type: text/html\n"

    db_connection = sqlite3.connect(DATABASE)
    cursor = db_connection.cursor()
    cursor.execute("CREATE TA


def main():
    rss_groups()


if __name__ == "__main__":
    main()
