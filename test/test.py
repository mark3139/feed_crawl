from feed import parse_rss, parse_atom


def rss():
    tests = ['http://robbinfan.com/rss', 'nanfang', 'http://coolshell.cn/feed']
    for test in tests:
        r = parse_rss(test)
        print r.title
        print r.des
        print r.link
        print r.lang
        for item in r.get_items():
            print item.title
            print item.link
            print item.des
            print item.pubdate


def atom():
    tests = ['atom.xml']
    for test in tests:
        a = parse_atom(test)
        print a.title
        print a.updated
        print a.subtitle
        print a.link
        for item in a.get_items():
            print item.title
            print item.link
            print item.published
            print item.updated
            print item.summary
            print item.category


if __name__ == '__main__':
    #rss()
    atom()
