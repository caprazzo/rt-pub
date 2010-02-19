import simplejson as json
from amqplib import client_0_8 as amqp
import threading
import time

def serialize(obj):
	return json.dumps(obj)

def deserialize(json_obj):
	return json.loads(json_obj)
		
class ResponseListener(threading.Thread):
		
	def setup(self):
		self.do_stop = False
		self.requests = {}
		self.conn = amqp.Connection(host="localhost:5672", userid="guest", password="guest", virtual_host="/", insist=False)
		self.chan = self.conn.channel()

		#TODO: queue declarations should go in a system-level setup
		self.chan.queue_declare(queue="po_box", durable=True, exclusive=False, auto_delete=False)
		self.chan.exchange_declare(exchange="sorting_room", type="direct", durable=True, auto_delete=False,)
		self.chan.exchange_declare(exchange="void", type="direct", durable=True, auto_delete=False,)

		self.chan.queue_bind(queue="po_box", exchange="sorting_room", routing_key="jason")
	
	def recv(self, msg):
		envelope = deserialize(msg.body)
		key = envelope['to']
		if key in self.requests:
			callback = self.requests[key]
			del self.requests[key]
			callback(msg.body)
			
	def run(self):
		self.chan.basic_consume(queue='po_box', no_ack=True, callback=self.recv)
		while not self.do_stop:
			self.chan.wait()
		self.chan.close()
		self.conn.close()
			
	def register_request(self, key, callback):
		self.requests[key] = callback
		
	def stop(self):
		self.do_stop = True
		
class MessageService(object):
	def __init__(self):
		self.conn = amqp.Connection(host="localhost:5672", userid="guest", password="guest", virtual_host="/", insist=False)
		self.chan = self.conn.channel()
		self.response_listener = ResponseListener()
		self.response_listener.setup()
		self.response_listener.start()
		
	def stop(self):
		self.chan.close()
		self.conn.close()
		self.response_listener.stop()
	
	def send_request(self, request_obj, callback):
		envelope = {
			#poor man's unique key
			'from': str(time.time()), 
			'body': request_obj
		}
		
		self.response_listener.register_request(envelope['from'], callback)
		msg = amqp.Message(serialize(envelope))
		msg.properties["delivery_mode"] = 2
		self.chan.basic_publish(msg,exchange="void",routing_key="jason")