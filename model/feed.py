#/usr/bin python
#-*-coding: utf8-*-

from sqlalchemy import Table
from sqlalchemy.orm import mapper

from db import meta, session


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


class Feeds(object):
    def __init__(self):
        self.session = session

    def is_exists(self, url):
        row = self.session.query(FeedsModel).filter(FeedsModel.link == url).first()
        return row.id if row else None

    def add(self, finfo):
        self.session.add(finfo)
        self.session.flush()


class Items(object):
    pass

if __name__ == '__main__':
    DB()
    f = Feeds()
    f.is_exists('http://robbinfan.com')
