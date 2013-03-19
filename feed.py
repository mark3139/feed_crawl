class Entry():
    pass


class Feed(object):
    def __init__(self, etree):
        self.path = etree
        self.title = self.get_meta('title')
        self.link = self.get_meta('link')
        self.des = self.get_meta('description')

    def get_meta(self, path):
        try:
            meta = self.path.find(path).text
        except AttributeError:
            meta = None
        return meta


class RssItem(Feed):
    def __init__(self, item):
        Feed.__init__(self, item)
        self.path = item
        self.category = self.get_meta('category')
        self.author = self.get_meta('author')
        self.pubdate = self.get_meta('pubDate')


class Rss(Feed):
    def __init__(self, node):
        Feed.__init__(self, node)
        self.lang = self.get_meta('language')

    def get_items(self):
        return [RssItem(item) for item in self.path.findall('item')]
