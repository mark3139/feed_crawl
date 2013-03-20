from lxml import etree

__all__ = ['parse_rss', 'parse_atom']


class Feed(object):
    def __init__(self, etree):
        self.path = etree

    def get_meta(self, path):
        try:
            meta = self.path.find(path).text
        except AttributeError:
            meta = None
        return meta

    @property
    def title(self):
        return self.get_meta('title')

    @property
    def link(self):
        return self.get_meta('link')

    @property
    def des(self):
        return self.get_meta('description')


class RssItem(Feed):
    def __init__(self, item):
        Feed.__init__(self, item)
        self.path = item
        self.category = self.get_meta('category')
        self.author = self.get_meta('author')
        self.pubdate = self.get_meta('pubDate')


class Rss(Feed):
    def __str__(self):
        return unicode("Title: %s Link: %s" % (self.title, self.link)).encode('utf8')

    def __init__(self, node):
        Feed.__init__(self, node)
        self.lang = self.get_meta('language')

    def get_items(self):
        return [RssItem(item) for item in self.path.findall('item')]


class AtomBase(Feed):
    def __unicode__(self):
        return "Title: %s" % self.title

    def __init__(self, node):
        Feed.__init__(self, node)
        self.path = node
        self.ns = {'ns': 'http://www.w3.org/2005/Atom'}

    def get_meta(self, path, tag=None):
        xpath = '%s:%s' % ('ns', path)
        try:
            if tag:
                meta = self.path.find(xpath, namespaces=self.ns).get(tag)
            else:
                meta = self.path.find(xpath, namespaces=self.ns).text
        except AttributeError, e:
            print e
            meta = None
        return meta

    @property
    def updated(self):
        return self.get_meta('updated')

    @property
    def link(self):
        return self.get_meta('link[@href]', 'href')


class AtomItem(AtomBase):
    def __init__(self, item):
        Feed.__init__(self, item)
        self.path = item
        self.ns = {'ns': 'http://www.w3.org/2005/Atom'}

    @property
    def pubdate(self):
        return self.get_meta('published')

    @property
    def des(self):
        return self.get_meta('summary')

    @property
    def category(self):
        return self.get_meta('category', 'term')

    @property
    def author(self):
        return self.get_meta('author/ns:name')


class Atom(AtomBase):
    def __str__(self):
        return unicode("Title: %s Link: %s" % (self.title, self.link)).encode('utf8')

    def __init__(self, node):
        Feed.__init__(self, node)
        self.ns = {'ns': 'http://www.w3.org/2005/Atom'}

    def get_items(self):
        return [AtomItem(item) for item in self.path.findall('ns:entry', namespaces=self.ns)]

    @property
    def subtitle(self):
        return self.get_meta('subtitle')


def parse_rss(path):
    parser = etree.XMLParser()
    r = Rss(etree.parse(path, parser).find('channel'))
    return r


def parse_atom(path):
    parser = etree.XMLParser()
    a = Atom(etree.parse(path, parser))
    return a
