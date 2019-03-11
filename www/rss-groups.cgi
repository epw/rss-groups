#! /usr/bin/env python3

import feedparser
import rss_io
import blogger

import cgi, cgitb
cgitb.enable()


def rss_groups():
    args = cgi.FieldStorage()

    print("Content-Type: text/xml\n")

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
    # DEEPLY BROKEN! Should actually handle UTF-8!
    print(xml.encode("ascii", "ignore").decode("ascii", "ignore"))


def main():
    rss_groups()


if __name__ == "__main__":
    main()
