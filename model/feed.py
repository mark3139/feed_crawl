#/usr/bin python
#-*-coding: utf8-*-
import datetime

from sqlalchemy import Table
from sqlalchemy.orm import mapper

from db import meta, session
from lib.misc import str_md5


class DB():
    def __init__(self):
        feeds = Table("feeds", meta, autoload=True)
        items = Table("items", meta, autoload=True)
        mapper(FeedsModel, feeds)
        mapper(ItemsModel, items)


class FeedsModel(object):
        pass


class ItemsModel(object):
    pass


class ModelBase(object):
    def __init__(self):
        self.session = session

    def add(self, finfo):
        self.session.add(finfo)
        self.session.flush()
        return finfo.id


class Feeds(ModelBase):
    def __init__(self):
        ModelBase.__init__(self)

    def is_exists(self, url):
        row = self.session.query(FeedsModel).filter(FeedsModel.link == url).first()
        return row.id if row else None

    def get_basic(self):
        return self.session.query(FeedsModel.id, FeedsModel.type, FeedsModel.user_link).all()

    def is_same(self, id, feed):
        title = feed.title
        des = feed.des
        if not des:
            des = ''
        hash = str_md5((title + des).encode('utf8'))
        rhash = self.session.query(FeedsModel.hash).filter(FeedsModel.id == id).one()[0]
        return True if hash == rhash else False

    def add(self, id, feed, u_url):
        finfo = FeedsModel()
        finfo.title = feed.title
        finfo.link = feed.link
        finfo.updated = getattr(feed, 'updated', None)
        finfo.type = type
        finfo.user_link = u_url
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
        self.session.add(finfo)
        self.session.flush()
        return finfo.id


class Items(ModelBase):
    def __init__(self):
        ModelBase.__init__(self)

    def add(self, fid, item):
        item_info = ItemsModel()
        item_info.title = item.title
        item_info.link = item.link
        item_info.des = item.des
        item_info.pubdate = item.pubdate
        item_info.fid = fid
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
            print 'ValueError'

        self.session.add(item_info)
        self.session.flush()
        return item_info.id

    def is_same(self, item):
        title = item.title
        des = item.des or ''
        hash = str_md5((title + des).encode('utf8'))
        rs = self.session.query(ItemsModel.id).filter(hash == ItemsModel.hash).first()
        return rs[0] if rs else None

if __name__ == '__main__':
    DB()
    f = Feeds()
    f.is_exists('http://robbinfan.com')
