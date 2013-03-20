import urllib2
import re

import memcache
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import sessionmaker

from lib.feed import parse_rss, parse_atom
from lib.misc import str_md5, str_to_unicode


class DB():
    def __init__(self):
        engine = create_engine('mysql://root:@localhost:3306/sk?charset=utf8', encoding="utf-8")
        engine.connect()
        meta = MetaData(engine)
        Session = sessionmaker()
        Session.configure(bind=engine)
        self.session = Session()
        self.feed = Table("feed", meta, autoload=True)


class MC():
    def __init__(self):
        self.mc = memcache.Client(['127.0.0.1:11211'], debug=0)


class Fetch():
    def __init__(self, url):
        self.url = url.rstrip('/')
        self.mc = MC().mc
        self.feed = DB().feed
        self.session = DB().session

    def is_exists(self):
        return self.mc.get(self.url)

    def get_type(self):
        rss = r'<rss version="2.0">'
        atom = r'<feed xmlns="http://www.w3.org/2005/Atom">'
        #head = urllib2.urlopen(self.url, timeout=10).read(200)
        head = open(self.url).read(200)
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
            print feed
        except KeyError, e:
            print e
            raise 'xxx'
        finfo = {
            'title': feed.title,
            'link': feed.link,
            'subtitle': getattr(feed, 'subtitle', ''),
            'image': getattr(feed, 'image', ''),
            'updated': getattr(feed, 'updated', None),
            'des': feed.des,
            'type': type,
            'hash': str_md5((feed.title + feed.des).encode('utf8'))
        }
        i = self.feed.insert()
        i.execute(finfo)


if __name__ == '__main__':
    db = DB()
    #f = Fetch('http://robbinfan.com/rss/')
    f = Fetch('test/nanfang')

    f.feed_info()
