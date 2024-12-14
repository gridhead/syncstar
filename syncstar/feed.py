from hashlib import sha256

import feedparser

from syncstar.base import show_time
from syncstar.config import standard


def read_feed(link: str) -> tuple[bool, dict]:
    """
    Reads a consolidated record of feeds collected from unit location

    :return: Procedure status and collected feeds
    """
    rslt = {
        "head": "UNOBTAINABLE",
        "desc": "UNOBTAINABLE",
        "data": {}
    }
    feed = feedparser.parse(link)

    if feed.bozo:
        return False, rslt

    rslt["head"] = feed.feed.get("title", "UNOBTAINABLE")
    rslt["desc"] = feed.feed.get("description", "UNOBTAINABLE")

    for indx, note in enumerate(feed.entries):
        rslt["data"][sha256(str(indx).encode()).hexdigest()] = {
            "head": note.title,
            "link": note.link,
            "date": note.get("published", "No date"),
            "summ": note.get("summary", "No summary")
        }

    return True, rslt


def create_result() -> dict:
    """
    Makes a consolidated record of feeds collected from various distinct locations

    :return: Dictionary consisting of feeds collected from multiple sources
    """
    rslt = {
        "time": show_time(),
        "data": {}
    }
    for item in standard.fdlist:
        rslt["data"][item] = read_feed(item)[1]
    return rslt
