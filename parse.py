import urllib2

from lxml import etree

from feed import Rss


def parse(path):
    parser = etree.XMLParser()
    r = Rss(etree.parse(path, parser).find('channel'))
    #print r.title
    #print r.des
    #print r.link
    #print r.lang
    #print r.get_items()[0].title
    return r



if __name__ == '__main__':
    tests = ['http://robbinfan.com/rss', 'nanfang', 'http://coolshell.cn/feed']
    for test in tests:
        r = parse(test)
        print r.title
        print r.des
        print r.link
        print r.lang
        for item in r.get_items():
            print item.title
            print item.link
            print item.des
            print item.pubdate


