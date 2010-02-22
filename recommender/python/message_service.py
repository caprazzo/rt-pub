import simplejson as json
from amqplib import client_0_8 as amqp
import threading
import time
import logging
log = logging.getLogger(__name__)
import uuid

def serialize(obj):
	return json.dumps(obj)
		
class MessageService(object):
	
	def __init__(self, open_amqp_conn, exchange, response_listener):
		log.info('Starting publishing service')
		self.exchange = exchange
		self.response_listener = response_listener
		self.conn = open_amqp_conn()
		self.chan = self.conn.channel()
			
	def stop(self):
		log.info('Stopping')
		self.chan.close()
		self.conn.close()
		
	def send_request(self, request_obj, callback):
		key = str(uuid.uuid4())
		env = { 'message_id': key,  'body': request_obj }
		
		self.response_listener.register_request(key, callback)
		
		msg = amqp.Message(serialize(env))
		msg.properties["delivery_mode"] = 1
		
		log.info('registered and published request [%s]' % env)
		
		self.chan.basic_publish(msg, exchange=self.exchange)