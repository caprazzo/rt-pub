import simplejson as json
from amqplib import client_0_8 as amqp
import threading
import time
import logging
log = logging.getLogger(__name__)

def serialize(obj):
	return json.dumps(obj)
		
class MessageService(object):
	
	def __init__(self, amqp_host, query_queue, publish_exchange, response_listener):
		
		log.info('Starting publishing service')
		self.amqp_host = amqp_host
		self.query_queue = query_queue
		self.publish_exchange = publish_exchange
		self.response_listener = response_listener
		self.setup_amqp()		
	
	def setup_amqp(self):
		
		self.conn = amqp.Connection(
			host=self.amqp_host,
			userid="guest", 
			password="guest",
			virtual_host="/",
			insist=False)
			
		self.chan = self.conn.channel()
		
		self.chan.queue_declare(
			queue=self.query_queue,
			durable=True,
			exclusive=False,
			auto_delete=False)
			
		self.chan.exchange_declare(
			exchange=self.publish_exchange,
			type="fanout",
			durable=True,
			auto_delete=False)
			
		self.chan.queue_bind(
			queue=self.query_queue,
			exchange=self.publish_exchange)
		
	def stop(self):
		log.info('Stopping')
		self.chan.close()
		self.conn.close()
		
	
	def send_request(self, request_obj, callback):
		
		envelope = {
			'message_id': str(time.time()), 
			'body': request_obj
		}
		
		self.response_listener.register_request(
			envelope['message_id'], callback)
		
		msg = amqp.Message(serialize(envelope))
		msg.properties["delivery_mode"] = 2
		log.info('registered and published request [%s]' % envelope)
		self.chan.basic_publish(msg, exchange=self.publish_exchange)
		
		