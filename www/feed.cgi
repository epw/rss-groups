#! /usr/bin/env python3

import feedgen
from feedgen.feed import FeedGenerator
import code

import cgi, cgitb
cgitb.enable()


ROOT = "https://eric.willisson.org/rss-groups/"
URL = ROOT + "feed.cgi"


def add_entry(fg, path, title, content):
    fe = fg.add_entry()
    url = ROOT + "feed/" + path
    fe.id(url)
    fe.link(href=url)
    fe.title(title)
    fe.description("One entry")
    fe.content(content)
    return fe


def feed():
    args = cgi.FieldStorage()

    print("Content-Type: text/xml\n")

    fg = FeedGenerator()
    fg.id(URL)
    fg.title("RSS Groups Text Feed")
    fg.subtitle("Build entirely by Python")
    fg.author({"name": "Eric Willisson", "email": "ericwillisson@gmail.com"})
    fg.link(href=URL, rel="self")
    fg.language("en")

    add_entry(fg, "1", "First Post", "First post full of content!")
    add_entry(fg, "2", "New Day", "Stuff happens when the Sun comes up")
    add_entry(fg, "3", "Another Page", "There is full <b>HTML/b> here.")

#    code.interact(local={"args": args, "fg": fg})
    print(fg.rss_str().decode("utf-8"))


def main():
    feed()


if __name__ == "__main__":
    main()
