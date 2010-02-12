import feedparser
import json
import jsonpickle
import urllib
import datetime
import threading
import time
import sys
import couch

from xml.dom import minidom

visited_items = set([])
visited_users = []
queue = ['04542763409539038815']
triples = set([])

def store(f, subj, pred, obj):
	f.write(json.dumps((subj, pred, obj)) + '\n')


def drill_user(user):
	for item in shared_items(user):		
		f = open('store.txt', 'a')
		store(f, item['id'], 'dc:title', item['title']) 
		store(f, user, 'cu:shares', item['id'])
		if item['id'] not in visited_items:
			visited_items.add(item['id'])
			for liker in item['likers']:
				store(f, liker, 'cu:likes', item['id'])
				if liker not in queue:
					queue.append(liker)
					
def run():
	while len(queue) > 0:
		user = queue.pop()
		if user in visited_users:
			continue
		visited_users.append(user)
		print 'users: %s items: %s queue: %s user: %s' % (len(visited_users), len(visited_items), len(queue), user)
		try:
			
			drill_user(user)
		except:
			print 'error'
		
from urllib import urlopen,quote_plus
from xml.dom import minidom
def shared_items(user_id):
	items = []
	feed_url = 'http://www.google.com/reader/public/atom/user/%s/state/com.google/broadcast' % user_id
	continuation = 0
	while True:
		xml = urlopen("%s?c=%s" % (feed_url, continuation)).read()
		dom = minidom.parseString(xml)		
		continuation = None
		for element in dom.childNodes[0].childNodes:
			item = {'id':None, 'title':None, 'likers':[]}
			if element.localName == 'continuation':
				continuation = element.firstChild.data
			elif element.localName == 'entry':
				for sube in element.childNodes:
					if sube.localName == 'id':
						item['id'] = sube.firstChild.data
					elif sube.localName == 'title':
						item['title'] = sube.firstChild.data
					elif sube.localName == 'likingUser':
						item['likers'].append(sube.firstChild.data)
			if item['id'] is not None:
				items.append(item)
						
		if continuation is None or len(items) > 2000:
			return items
		else:
			print 'continue %s' % len(items)
				
run()