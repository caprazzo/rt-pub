# usage: python stats_copy.py <source_server> <target_server> <target_database> <delay>
# example store localhosts _stats on localhost:5984/stats every 60 seconds:
# $ python stats_copy.py localhost localhost stats 60
import httplib
import time
from datetime import datetime
import threading
import sys
try:
	import json
except ImportError:
	import simplejson as json
import random
import string

def rnd(size):
	return ''.join([random.choice(string.letters + string.digits) for i in xrange(size)])


class Db:
	def __init__(self, couch, db):
		self.couch = couch
		self.db = db

	def put(self, id, body):
		uri = '/%s/%s' % (self.db, id)
		return self.couch.put(uri, body)

	def putnew(self, body):
		return self.couch.putnew(self.db, body)
	
class Couch:
	"""Basic wrapper class for operations on a couchDB"""
	def __init__(self, host, port=5984):
		self.host = host
		self.port = port

	def connect(self):
		return httplib.HTTPConnection(self.host, self.port) # No close()
		
	def put(self, uri, body):
		c = self.connect()
		headers = {"Content-type": "application/json"}
		c.request("PUT", uri, body, headers)
		return c.getresponse()
		
	def get(self, uri):
		c = self.connect()
		headers = {"Accept": "application/json"}
		c.request("GET", uri, None, headers)
		return c.getresponse()
		
	def putnew(self, db, body):
		id = rnd(5)		
		result = json.loads(self.put("/%s/%s" % (db, id), body).read())		
		if "error" in result:
			if result["error"] == "conflict":
				throw("conflict %s" % id)
				return self.putnew(db, body)
			else:
				throw(result["error"])
		return id

