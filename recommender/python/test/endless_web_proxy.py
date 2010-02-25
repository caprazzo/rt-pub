import tornado.httpserver
import tornado.ioloop
import tornado.web
import time
import threading
import urllib

def respond(handler, prefix):
	handler.write('cazzi\n')
	count=0
	while True:
		handler.write('%d\n' % count)
		count += 1
		handler.flush()
		time.sleep(0.5)
	handler.finish()

class MainHandler(tornado.web.RequestHandler):
	@tornado.web.asynchronous
	def get(self):
		prefix = self.get_parameter('prefix')
		self.write("Hello, world")
		threading.Thread(target=respond,args=[self, prefix]).start()

application = tornado.web.Application([
    (r"/", MainHandler),
])

if __name__ == "__main__":
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(8888)
    tornado.ioloop.IOLoop.instance().start()