#! /usr/bin/env python3

import datetime
import PyRSS2Gen


def feedparser_to_pyrss2gen(parsed):
    items = [PyRSS2Gen.RSSItem(
        title = entry.title,
        link = entry.link,
        description = entry.content[0].value,
#        description = "entry.content[0]",
        guid = entry.link,
        pubDate = datetime.datetime(
            entry.published_parsed[0],
            entry.published_parsed[1],
            entry.published_parsed[2],
            entry.published_parsed[3],
            entry.published_parsed[4],
            entry.published_parsed[5]))
             for entry in parsed.entries]
    rss = PyRSS2Gen.RSS2(
        title = parsed.feed.title,
        link = parsed.feed.link,
        description = parsed.feed.description,
#        description = "parsed.feed.description",
        lastBuildDate = datetime.datetime.now(),
        items = items)
    return rss.to_xml(encoding="utf-8")

             
