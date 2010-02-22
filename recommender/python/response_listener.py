import simplejson as json
from amqplib import client_0_8 as amqp
import threading
import time
import logging
log = logging.getLogger(__name__)



def deserialize(json_obj):
	return json.loads(json_obj)
	
class ResponseListener(threading.Thread):
	"""
	Listens for messages on a queue and if a callback has been registered to message.body.message_id,
	the callback is executed and the message removed from the queue.
	"""
	
	def __init__(self, open_amqp_conn, queue):
		log.info('Starting response listener')
		threading.Thread.__init__(self)
		self.open_amqp_conn = open_amqp_conn
		self.queue = queue
		self.do_stop = False
		self.requests = {}

	def recv(self, msg):
		envelope = deserialize(msg.body)
		key = envelope['message_id']
		log.info('received message with key %s: %s' % (key, envelope))
		if key in self.requests:
			log.info('found callback for message %s. dispatching.' % key)
			self.chan.basic_ack(msg.delivery_tag)
			callback = self.requests[key]
			del self.requests[key]
			callback(msg.body)
			
	def run(self):
		conn = self.open_amqp_conn()
		chan = conn.channel()
		log.info('Start consuming queue %s' % self.queue)	
		try:
			chan.basic_consume(queue=self.queue, no_ack=False, callback=self.recv)
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