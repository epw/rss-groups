#! /usr/bin/env python3

import datetime
import PyRSS2Gen as RSS2
import pytz


def rss2_item_from_entry(entry):
    return RSS2.RSSItem(
        title = entry.title,
#        title = entry.title,
        link = entry.link,
        description = entry.content[0].value,
#        description = "entry.content[0]",
        author = entry.author + " <email@example.com>",
        guid = entry.link,
        pubDate = datetime.datetime(
            entry.published_parsed[0],
            entry.published_parsed[1],
            entry.published_parsed[2],
            entry.published_parsed[3],
            entry.published_parsed[4],
            entry.published_parsed[5]).replace(tzinfo=pytz.utc))


def feedparser_to_rss2(title, link, description, entries, rssentries):
    items = [rss2_item_from_entry(entry) for entry in entries]
    items.extend(rssentries)
    items.sort(key=lambda i: i.pubDate)
    items.reverse()
    rss = RSS2.RSS2(
        title = title,
        link = link,
        description = description,
        lastBuildDate = datetime.datetime.now(),
        items = items)
    return rss.to_xml(encoding="utf-8")
