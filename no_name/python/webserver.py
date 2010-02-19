import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.httpclient
import time
from tornado.options import define, options
from message_service import MessageService
from response_listener import ResponseListener
import logging
log = logging.getLogger(__name__)


class SearchHandler(tornado.web.RequestHandler):
	
	def __init__(self, application, request, message_service):
		tornado.web.RequestHandler.__init__(self,application, request)
		self.message_service = message_service

	@tornado.web.asynchronous
	def get(self):
		query=self.get_argument('q')
		log.info('received search query [%s]' % query)
		self.message_service.send_request({'web-query':query},
			self.async_callback(self.on_response))

	def on_response(self, response):
		log.info('received response [%s]' % response)
		self.write("Received " + response)
		self.finish()

def main():
	log.info('Web system start')	
	tornado.options.parse_config_file('system_conf.py')
	tornado.options.parse_command_line()
	
	response_listener = ResponseListener(
		amqp_host=options.amqp_host,
		response_queue=options.response_queue)
	
	message_service = MessageService(
		amqp_host=options.amqp_host,
		query_queue=options.query_queue,
		publish_exchange=options.web_query_exchange,
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
