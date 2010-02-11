import couch
try:
	import json
except ImportError:
	import simplejson as json

c = couch.Couch('couch.caprazzi.net', port=80)
posts = json.loads(c.get('/posts/_design/app/_view/posts_by_date?descending=true&limit=32').read())

db = couch.Db(c, 'posts')


for p in posts['rows']:
	#print p['value']['url']
	shortdoc = db.putnew(json.dumps({
		'url': p['value']['url'],
		'type': 'shorturl'
	}))
	#print shortdoc
	shorturl = u'http://couch.caprazzi.net/posts/%s' % shortdoc
	tweet = p['value']['body'][:-(len(shorturl)+1)] + ' ' + shorturl
	#print
	#print len(tweet)
	print (u'%s' % tweet).encode('utf-8')
	#print

# for i in xrange(0,700):
#	print i
	
# get 700 short messages from couchdb
# curl 'http://couch.caprazzi.net/posts/_design/app/_view/posts_by_date?descending=true&limit=720'

# for each one generate a short url

# and save the result in a file
