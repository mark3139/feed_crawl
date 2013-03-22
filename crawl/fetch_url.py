#/usr/bin python
#-*-coding: utf8-*-
import re
import urllib2
import logging
from datetime import datetime

import memcache

from lib.feed import parse_rss, parse_atom
from lib.misc import str_md5
from model.feed import Feeds, Items, DB, FeedsModel, ItemsModel


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
        logging.info("URL:%s, HEAD:%s", self.url, head)
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
            logging.exception(e)
            return 0
        finfo = FeedsModel()
        finfo.title = feed.title
        finfo.link = feed.link
        finfo.updated = getattr(feed, 'updated', None)
        finfo.type = type
        finfo.user_link = self.url
        im = getattr(feed, 'image', '')
        st = getattr(feed, 'subtitle', '')
        if im:
            finfo.image = im
        if st:
            finfo.subtitle = st
        if feed.des:
            finfo.des = feed.des
        if not finfo.des:
            feed.des = ''
        finfo.hash = str_md5((feed.title + feed.des).encode('utf8'))
        lastid = self.feeds.add(finfo)

        #self.mc.set(self.url, row.lastrowid)

        for item in feed.get_items():
            item_info = ItemsModel()
            item_info.title = item.title
            item_info.link = item.link
            item_info.des = item.des
            item_info.pubdate = item.pubdate
            item_info.fid = lastid
            if item.author:
                item_info.author = item.author
            if item.category:
                item_info.category = item.category
            if not item.des:
                item_info.hash = str_md5((item_info.title).encode('utf8'))
            else:
                item_info.hash = str_md5((item_info.title + item_info.des).encode('utf8'))
            try:
                dt = datetime.strptime(item_info.pubdate[0: -6], "%a, %d %b %Y %H:%M:%S")
                item_info.pubdate = dt.strftime("%Y-%m-%d %H:%M:%S")
            except ValueError:
                pass

            self.items.add(item_info)
        return lastid

    def fetch_url(self):
        id = self.is_exists()
        return id if id else self.feed_info()

if __name__ == '__main__':
    logging.basicConfig(filename='err.log', level=logging.DEBUG)
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
            f = Fetch(url)
            print f.fetch_url()
        except Exception, e:
            logging.exception(e)
