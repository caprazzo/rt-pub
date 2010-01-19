import feedparser
import json
import jsonpickle
import urllib
import datetime
import threading
import time
import sys
import couch

import logging
import logging.config
import ConfigParser
import hashlib

logging.config.fileConfig('logging.conf')
			
class Fetcher:
	def __init__(self, feed_url, feed_name, db):
		self.feed_url = feed_url
		self.db = db
		self.feed_name = feed_name
		self.log = logging.getLogger('fetcher-%s' % (feed_name))

	def start(self):
	    continuation = 0
	    timestamp = 0
	    while True:
	        self.log.info('fetch feed - last update: %s' % (timestamp))
	        d = feedparser.parse("%s?c=%s" % (feed_url, continuation))
	        if continuation <> 0 or d.feed.updated > timestamp:
	            timestamp = d.feed.updated
	            self.log.info('continuation: %s, last update: %s' % (continuation, timestamp))
	            rt = self.store_posts(d.entries)
	            if rt is False:
	                self.log.info('encountered existing doc - feed up-to-date')
	                time.sleep(10)
	            else:
	                self.log.info('fetch consumed all items, going back in time')
	                if 'gr_continuation' in d.feed:
	                    continuation = d.feed.gr_continuation
	                else:
	                    continuation = 0
    	            time.sleep(2)
	        else:
				self.log.info('no action')
				time.sleep(60)

	def put(self, id, post):
		return json.loads(self.db.put(id, jsonpickle.encode(post)).read())


	def store(self, post):
		post['fetcher'] = { 'app-type': 'shared-items-post', 'feed_name': self.feed_name}
		_id = hashlib.md5(post.id).hexdigest()
		response = self.put(_id, post)
		if 'error' in response:
			if response['error'] == 'conflict':
				return False
			else:
				self.log.critical('unhandled response %s' % (response))
				trhow(json.dumps(response))
		return True

	def store_posts(self, posts):
		for post in posts:
			rt = self.store(post)
			if rt is False:
				self.log.info('encountered existing doc - stop scanning list')
				return False
		return True

def fetch(feed_url, feed_name, db):
	f = Fetcher(feed_url, feed_name, db)
	f.start()

if __name__ == "__main__":
	cfg = ConfigParser.ConfigParser()
	cfg.read('configuration.conf')
	couch_srv = cfg.get('Fetcher', 'couch_srv')
	couch_db = cfg.get('Fetcher', 'couch_db')
	srv = couch.Couch(couch_srv)
	db = couch.Db(srv, couch_db)
	feeds = cfg.get('Fetcher','feeds')
	for feed_name in [ feed.strip() for feed in feeds.split(',')]:
		feed_url = cfg.get('feed_%s' % (feed_name), 'url')	
		threading.Thread(target=fetch, args=[feed_url, feed_name, db]).start()
		print 'started'

