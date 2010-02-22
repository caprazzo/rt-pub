import tornado
import tornado.ioloop
from tornado.options import options
import threading
from amqplib import client_0_8 as amqp
import simplejson as json

tornado.options.parse_config_file('system_conf.py')
tornado.options.parse_command_line()
import logging
log = logging.getLogger(__name__)

def handle_request(response):
	if response.error:
		print "Error:", response.error
	else:
		print response.body
	#tornado.ioloop.IOLoop.instance().stop()
	
class QueueListener(threading.Thread):

	def __init__(self, open_amqp_conn, queue):
		log.info('Starting response listener')
		threading.Thread.__init__(self)
		self.open_amqp_conn = open_amqp_conn
		self.queue = queue
		self.do_stop = False
		self.requests = {}

	def recv(self, msg):
		envelope = deserialize(msg.body)
		key = envelope['response_to_id']
		log.info('received message with key %s: %s' % (key, envelope))
		if key in self.requests:
			log.info('found callback for message %s. dispatching.' % key)
			callback = self.requests[key]
			del self.requests[key]
			callback(msg.body)

	def run(self):
		conn = self.open_amqp_conn()
		chan = conn.channel()
		log.info('Start consuming queue %s' % self.queue)	
		try:
			chan.basic_consume(queue=self.queue, no_ack=True, callback=self.recv)
			while not self.do_stop:
				chan.wait()
		except Exception, e:
			log.error('Exception [%s]', str(e))
		log.info('Stopping')
		chan.close()
		conn.close()

	def register_request(self, key, callback):
		log.info('registered callback for request [%s]' % key)
		self.requests[key] = callback

	def stop(self):
		self.do_stop = True

class Webclient(threading.Thread):
	
	def run(self):
		log.info('starting httplient ioloop')
		tornado.ioloop.IOLoop.instance().start()
	
	def wrap(self, callback):
		def wrapper(response):
			log.info('executing callback')
			callback(response)
		return wrapper
	
	def fetch(self, url, callback):
		log.info('fetching url [%s]' % url)
		self.http_client = tornado.httpclient.AsyncHTTPClient()
		self.http_client.fetch(url, self.wrap(callback))
		
	def stop(self):
		log.info('stopping')
		tornado.ioloop.IOLoop.instance().stop()

def recv(msg):
	obj = json.loads(msg.body)
	log.info('received [%s]' % obj)

def setup_amqp(self):
	
def umain():
	q = QueueListener(get_amqp_conn, 'initial_query_queue')
	c = WebClient()
	
	def amqp_respond(message_id, profiles):
		env = {
			'response_to_id': message_id,
			'body': {
				'web-query': profiles
			}
		}
		# put it on query_queue
		
	def amqp_recv(message):
		obj = json.loads(message.body)
		message_id = obj['message_id']
		profile = obj.body['web-query']
		url = 'http://socialgraph.apis.google.com/otherme?q=%s' % profile
		
		def http_recv(response):
			social_graph = json.loads(response.body)
			others = social_graph.keys()
			others.append[profile]
			amqp_respond(message_id, others)
			
		c.fetch(url, http_recv)
		
	q.onMessage(amqp_recv)
	q.start()
		

def main():
	log.info('starting main')	
	web_client = Webclient()
	web_client.start()
	
	conn = amqp.Connection(host=self.amqp_host,
		userid="guest", password="guest",
		virtual_host="/", insist=False)
		
	chan = conn.channel()
	try:	
		chan.basic_consume(queue='initial_query_queue',
			no_ack=True,
			callback=recv)
		
		while True:
			chan.wait()
	except:
		log.error()	
	conn.stop()
	chan.stop()
	
if __name__ == "__main__":
	main()