#/usr/bin python
#-*-coding: utf8-*-
from model.feed import Feeds, DB, Items
from lib.feed import parse_rss, parse_atom
from lib.misc import setlog


def update():
    feeds = Feeds()
    items = Items()
    for (id, type, link) in feeds.get_basic():
        print id, type, link
        parse_m = parse_rss if type == 'rss' else parse_atom
        feed = parse_m(link)
        if not feeds.is_same(id, feed):
            for item in feed.get_items():
                if not items.is_same(item):
                    items.add(id, item)


if __name__ == '__main__':
    log = setlog(filename='log/update.log')
    DB()
    update()
