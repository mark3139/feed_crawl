import re
import urllib2
import logging
from datetime import datetime

import memcache
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import sessionmaker

from lib.feed import parse_rss, parse_atom
from lib.misc import str_md5


class DB():
    def __init__(self):
        engine = create_engine('mysql://root:@localhost:3306/sk?charset=utf8', encoding="utf-8")
        engine.connect()
        meta = MetaData(engine)
        Session = sessionmaker()
        Session.configure(bind=engine)
        self.session = Session()
        self.feeds = Table("feeds", meta, autoload=True)
        self.items = Table("items", meta, autoload=True)


class MC():
    def __init__(self):
        self.mc = memcache.Client(['127.0.0.1:11211'], debug=0)


class Fetch():
    def __init__(self, url):
        self.url = url.rstrip('/')
        self.mc = MC().mc
        self.feeds = DB().feeds
        self.items = DB().items
        self.session = DB().session

    def is_exists(self):
        id = self.mc.get(self.url)
        if id:
            return id
        else:
            s = self.feeds.select(self.feeds.c.user_link == self.url)
            row = s.execute().fetchone()
            return row.id if row else None

    def get_type(self):
        rss = r'<rss version="2.0"|<rss xmlns'
        atom = r'<feed xmlns="http://www.w3.org/2005/Atom">'
        #head = open(self.url).read(1000)
        head = urllib2.urlopen(self.url, timeout=10).read(200)
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
        finfo = {
            'title': feed.title,
            'link': feed.link,
            'updated': getattr(feed, 'updated', None),
            'type': type,
            'user_link': self.url
        }
        im = getattr(feed, 'image', '')
        st = getattr(feed, 'subtitle', '')
        if im:
            finfo['image'] = im
        if st:
            finfo['subtitle'] = st

        if feed.des:
            finfo['des'] = feed.des
        if not finfo.get('des'):
            finfo['hash'] = str_md5((feed.title).encode('utf8'))
        else:
            finfo['hash'] = str_md5((feed.title + feed.des).encode('utf8'))

        i = self.feeds.insert()
        row = i.execute(finfo)

        self.mc.set(self.url, row.lastrowid)

        items = []
        for item in feed.get_items():
            item_dc = {
                'title': item.title,
                'link': item.link,
                'des': item.des,
                #'des': '',
                'pubdate': item.pubdate,
                'fid': row.lastrowid
            }
            if item.author:
                item_dc['author'] = item.author

            if item.category:
                item_dc['category'] = item.category

            if not item_dc['des']:
                item_dc['hash'] = str_md5((item_dc['title']).encode('utf8'))
            else:
                item_dc['hash'] = str_md5((item_dc['title'] + item_dc['des']).encode('utf8'))
            try:
                dt = datetime.strptime(item_dc['pubdate'][0: -6], "%a, %d %b %Y %H:%M:%S")
                item_dc['pubdate'] = dt.strftime("%Y-%m-%d %H:%M:%S")
            except ValueError:
                pass
            items.append(item_dc)
           # print item_dc
        i = self.items.insert()
        i.execute(items)
        return row.lastrowid

    def fetch_url(self):
        id = self.is_exists()
        return id if id else self.feed_info()

if __name__ == '__main__':
    logging.basicConfig(filename='err.log', level=logging.DEBUG)
    db = DB()
    #f = Fetch('http://robbinfan.com/rss/')
    test_urls = [
        'http://robbinfan.com/rss',
        'http://www.ruanyifeng.com/blog/atom.xml',
        'http://shell909090.com/blog/feed/',
        'http://digdeeply.org/feed',
        'http://www.read.org.cn/feed',
        'http://feed.feedsky.com/nosqlfan',
        'http://feed.feedsky.com/aqee-net',
        'http://feed.feedsky.com/programmer',
        'http://cnpolitics.org/feed/'
        '../test/robin',
        '../test/feedsky'
    ]
    for url in test_urls:
        try:
            f = Fetch(url)
            print f.fetch_url()
        except Exception, e:
            logging.exception(e)
