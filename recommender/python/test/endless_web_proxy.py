import tornado.httpserver
import tornado.ioloop
import tornado.web
import time
import threading
import urllib
import memcache

def pick(name, cache, mc):
	if name in cache:
		return cache[name]

	id = mc.get(name)
	cache[name] = id
	return id
	
def pk(name, mc):
	id = mc.get(name)
	
def increment(mc):
	count = mc.get('unique_counter')
	if count is not None:
		mc.incr('unique_counter')
		return count
	mc.set('unique_counter', "1")
	return "0"
	
def respond(handler, prefix):
	handler.write('cazzi\n')
	count=0
	mc = memcache.Client(['127.0.0.1:11211'], debug=0)
	
	if 
	req = urllib.urlopen('http://localhost:8889/?prefix=%s' % prefix)
	#users_cache = {}
	#items_cache = {}
	
	for line in req:
		user, item = [re.sub('^.*/','',t).strip() for t in re.sub('[<>]', '', line).split('\t')]
		#user_id = pick(user, users_cache, mc)
		#item_id = pick(item, items_cache, mc)
		user_id = mc.get(user)
		item_id = mc.get(item)
		handler.write('%s,%s\n' % (user_id,item_id))
		handler.flush()
		
	handler.finish()

class MainHandler(tornado.web.RequestHandler):
	@tornado.web.asynchronous
	def get(self):
		prefix = self.get_argument('prefix')
		self.write("Hello, world")
		threading.Thread(target=respond,args=[self, prefix]).start()

application = tornado.web.Application([
    (r"/", MainHandler),
])

if __name__ == "__main__":
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(8888)
    tornado.ioloop.IOLoop.instance().start()