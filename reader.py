from urllib import urlopen
from xml.dom import minidom
import logging
import logging.config
import sys, traceback

logging.config.fileConfig('logging.conf')
log = logging.getLogger('reader')

class Reader:
	
	def user_feed_url(self, user_id):
		return 'http://www.google.com/reader/public/atom/user/%s/state/com.google/broadcast' % user_id

	def drill_user(self, user):

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
						
	def shared_items(self, user_id, page_size=1000, max=3000):
		try:
			log.info('fetching user %s' % user_id)
			feed_url = self.user_feed_url(user_id)
			print feed_url
			count = 0
			continuation = 0
			while continuation <> None:
				xml = urlopen("%s?c=%s&n=%s" % (feed_url, continuation, page_size)).read()

				dom = minidom.parseString(xml)
				log.debug('got continuation %s, %d bytes' % (continuation, len(xml)))
				continuation = None
				for element in dom.childNodes[0].childNodes:
					if element.localName == 'continuation':
						continuation = element.firstChild.data
					elif element.localName == 'entry':
						yield element
						count += 1
						if count >= 3000:
							return
		except Exception, e:
			print e
			return
			
		return