import simplejson as json
from amqplib import client_0_8 as amqp
import threading
import time
import logging
log = logging.getLogger(__name__)

def deserialize(json_obj):
	return json.loads(json_obj)
	
class ResponseListener(threading.Thread):
	
	def __init__(self, amqp_host, response_queue):
		self.log = logging.getLogger(self.__class__.__name__)
		self.log.info('Starting response listener')
		threading.Thread.__init__(self)
		self.amqp_host = amqp_host
		self.response_queue = response_queue
		
	def setup_amqp(self):
		self.do_stop = False
		self.requests = {}
		
		self.conn = amqp.Connection(
			host=self.amqp_host,
			userid="guest", password="guest",
			virtual_host="/",
			insist=False)
			
		self.chan = self.conn.channel()

		self.chan.queue_declare(
			queue=self.response_queue,
			durable=True,
			exclusive=False,
			auto_delete=False)

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
		
		self.setup_amqp()
		self.chan.basic_consume(
			queue=self.response_queue,
			no_ack=True,
			callback=self.recv)
		log.info('Started recv loop on queue %s' % self.response_queue)	
		while not self.do_stop:
			self.chan.wait()
		self.log.info('Stopping')
		self.chan.close()
		self.conn.close()
			
	def register_request(self, key, callback):
		log.info('registered callback for request [%s]' % key)
		self.requests[key] = callback
		
	def stop(self):
		self.do_stop = True