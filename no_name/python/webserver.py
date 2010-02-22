import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.httpclient
import time
from tornado.options import define, options
from message_service import MessageService
from response_listener import ResponseListener
from amqplib import client_0_8 as amqp
from system_conf import open_amqp_conn
import logging
log = logging.getLogger(__name__)
		
class SearchHandler(tornado.web.RequestHandler):
	
	def __init__(self, application, request, message_service):
		tornado.web.RequestHandler.__init__(self,application, request)
		self.message_service = message_service
		self.ioloop = tornado.ioloop.IOLoop.instance()

	@tornado.web.asynchronous
	def get(self):
		query = self.get_argument('q')
		log.info('received search query [%s]' % query)
		deadline = time.time() + options.web_query_timeout
		self.timeout = self.ioloop.add_timeout(deadline, self.on_timeout)
		self.message_service.send_request({'web-query':query}, self.async_callback(self.on_response))

	def on_response(self, response):
		log.info('received response [%s]' % response)
		self.ioloop.remove_timeout(self.timeout)
		self.write("Received " + response)
		self.finish()		
			
	def on_timeout(self):
		log.warn('timeout')
		self.write('timeout')
		self.finish()

def main():
	log.info('Web system start')	
	tornado.options.parse_command_line()
	
	response_listener = ResponseListener(open_amqp_conn, queue='response_queue')
	
	message_service = MessageService(open_amqp_conn,
		exchange='initial_query_exchange',
		response_listener=response_listener)
    	
	application = tornado.web.Application([
		(r"/search", SearchHandler, {"message_service":message_service})
	])
	
	http_server = tornado.httpserver.HTTPServer(application)
	http_server.listen(options.web_server_port)

	response_listener.start()
	log.info('Starting web server on port %d' % options.web_server_port)			
	
	try:		
		tornado.ioloop.IOLoop.instance().start()
	except:
		response_listener.stop()		
		message_service.stop()
		exit()
    	
if __name__ == "__main__":
    main()
