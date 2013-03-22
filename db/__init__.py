from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker

engine = create_engine('mysql://root:@localhost:3306/sk?charset=utf8', encoding="utf-8")
print 'connect'
engine.connect()

meta = MetaData(engine)
Session = sessionmaker(engine)
session = Session()
        #self.feeds = Table("feeds", meta, autoload=True)
        #self.items = Table("items", meta, autoload=True)
        #mapper(Feeds, self.feeds)
        #mapper(Items, self.items)
        #return self.session
