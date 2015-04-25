from datetime import datetime
from werkzeug.contrib.atom import AtomFeed, FeedEntry

def gen_feed(feed_url, url, songlist):
    feed = AtomFeed('Songlist', feed_url=feed_url, url=url)
    for s in songlist:
        feed.add(title=s['title'], content=s['url'],
            summary=s['other'], url=s['url'],
            updated=datetime(*s['time'][:6]), author=s['submitter'])
    return feed
