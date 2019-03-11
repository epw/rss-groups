#! /usr/bin/env python3

import feedparser
import rss_io

import cgi, cgitb
cgitb.enable()


def rss_groups():
    args = cgi.FieldStorage()

    print("Content-Type: text/xml\n")

    parsed = feedparser.parse("https://hackaday.com/blog/feed/")
    print(rss_io.feedparser_to_pyrss2gen(parsed))


def main():
    rss_groups()


if __name__ == "__main__":
    main()
