import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.httpclient
import threading
import time
import random
from tornado.options import define, options


class Delay(threading.Thread):
	
	def __init__(self, kb):
		threading.Thread.__init__(self)
		self.kb = kb
		self.start()
		
	def run(self):
		time.sleep(random.randint(0,2))
		self.kb()
	
class BogusGraphApi(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(self):
		print 'ping'
		Delay(self.respond)

    def respond(self):
		self.write('{"bogus":"bogus"}')
		self.finish()


def main():
	application = tornado.web.Application([
		(r"/otherme", BogusGraphApi)
	])
	http_server = tornado.httpserver.HTTPServer(application)
	http_server.listen(1234)
	tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()