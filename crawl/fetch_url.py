#/usr/bin python
#-*-coding: utf8-*-
import re
import urllib2

import memcache

from lib.feed import parse_rss, parse_atom
from lib.misc import setlog
from model.feed import Feeds, Items, DB


class MC():
    def __init__(self):
        self.mc = memcache.Client(['127.0.0.1:11211'], debug=0)


class Fetch():
    def __init__(self, url):
        self.url = url.rstrip('/')
        self.mc = MC().mc
        self.feeds = Feeds()
        self.items = Items()

    def is_exists(self):
        id = self.mc.get(self.url)
        if id:
            return id
        else:
            return self.feeds.is_exists(self.url)

    def get_type(self):
        rss = r'<rss version="2.0"|<rss xmlns'
        atom = r'<feed xmlns="http://www.w3.org/2005/Atom">'
        head = open(self.url).read(1000)
        #head = urllib2.urlopen(self.url, timeout=10).read(200)
        log.debug("URL:%s, HEAD:%s", self.url, head)
        if re.search(rss, head):
            return 'rss'
        elif re.search(atom, head):
            return 'atom'
        else:
            return None

    def feed_info(self):
        type = self.get_type()
        pm = {
            'rss': parse_rss,
            'atom': parse_atom
        }
        try:
            feed = pm[type](self.url)
        except KeyError, e:
            log.exception(e)
            return 0
        lastid = self.feeds.add(feed, self.url, type)

        #self.mc.set(self.url, row.lastrowid)

        for item in feed.get_items():
            self.items.add(lastid, item)
        return lastid

    def fetch_url(self):
        id = self.is_exists()
        return id if id else self.feed_info()

if __name__ == '__main__':
    log = setlog(filename='log/fetch.log')
    log.info('start')
    #f = Fetch('http://robbinfan.com/rss/')
    DB()
    test_urls = [
        #'http://robbinfan.com/rss',
        #'http://www.ruanyifeng.com/blog/atom.xml',
        #'http://shell909090.com/blog/feed/',
        #'http://digdeeply.org/feed',
        #'http://www.read.org.cn/feed',
        #'http://feed.feedsky.com/nosqlfan',
        #'http://feed.feedsky.com/aqee-net',
        #'http://feed.feedsky.com/programmer',
        #'http://cnpolitics.org/feed/'
        '../test/robin',
        #'../test/feedsky'
    ]
    for url in test_urls:
        try:
            log.info('URL:%s', url)
            f = Fetch(url)
        except Exception, e:
            log.exception(e)
