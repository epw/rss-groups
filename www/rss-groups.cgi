#! /usr/bin/env python3

import feedparser
import rss_io
import blogger
import locale

import cgi, cgitb
cgitb.enable()

def rss_groups():
    args = cgi.FieldStorage()

    print("Content-Type: text/xml; charset=utf-8\n")

    parsed = feedparser.parse("https://hackaday.com/blog/feed/")
    entries = parsed.entries
    parsed = feedparser.parse("http://feeds.arstechnica.com/arstechnica/index")
    entries.extend(parsed.entries)

    try:
        rssentries = blogger.rss()
    except blogger.client.AccessTokenRefreshError:
        print ('<?xml version="1.0"><error>The credentials have been revoked or expired, please re-run'
               'the application to re-authorize</error>')
        exit()
    
    xml = rss_io.feedparser_to_rss2("Combined Hackaday and Ars Technica",
                                    "https://eric.willisson.org/rss-groups/rss-groups.cgi",
                                    "First try at a combined feed",
                                    entries, rssentries)

    # If you're getting weird UnicodeDecode errors, then use this temporarily.
    # You'll have to edit the server to change the environment variables to LANG=en_US.UTF-8
    #    print(xml.encode("ascii", "namereplace").decode("ascii", "namereplace"))
    print(xml)


def main():
    rss_groups()


if __name__ == "__main__":
    main()
