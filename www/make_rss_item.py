#! /usr/bin/env python3

import PyRSS2Gen as RSS2
import dateparser
import pytz


def get_author(blog_name, author_name):
    if author_name:
        return blog_name + " - " + author_name
    return blog_name


def get_pubdate(pubdate):
    if type(pubdate) == str:
        return dateparser.parse(pubdate).replace(tzinfo=pytz.utc)
    return pubdate


def make_item(title, blog_name, author_name, url, content, pubdate):
    return RSS2.RSSItem(
        title=title,
        author=get_author(blog_name, author_name),
        link=url,
        description=content,
        guid=url,
        pubDate=get_pubdate(pubdate))
