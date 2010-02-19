import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.httpclient
import time
from tornado.options import define, options
from bus import MessageService

define("port", default=8888, help="run on the given port", type=int)   

class MainHandler(tornado.web.RequestHandler):
	
	def __init__(self, application, request, message_service):
		tornado.web.RequestHandler.__init__(self,application, request)
		self.message_service = message_service

	@tornado.web.asynchronous
	def get(self):
		query=self.get_argument('q')
		self.message_service.send_request({'web-query':query}, self.on_response)

	def on_response(self, response):
		self.write("Response to " + self.requested + ': ' + response)
		self.finish()

def main():
    tornado.options.parse_command_line()
    message_service = MessageService()
    application = tornado.web.Application([
        (r"/search", MainHandler, {"message_service":message_service})
    ])
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    
    try:
    	tornado.ioloop.IOLoop.instance().start()
    except:
        message_service.stop()
        exit()
    	
if __name__ == "__main__":
    main()
