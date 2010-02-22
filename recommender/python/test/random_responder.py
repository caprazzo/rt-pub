from amqplib import client_0_8 as amqp
import tornado
from tornado.options import options
from system_conf import open_amqp_conn
import threading
tornado.options.parse_command_line()
import simplejson as json
import time
import random
conn = open_amqp_conn()
	
chan = conn.channel()
chan.exchange_declare(exchange='stupid_client_exchange', type="fanout")
chan.queue_bind(queue='response_queue', exchange='stupid_client_exchange')
	
class RandomRespond(threading.Thread):

	def __init__(self, in_msg):
		threading.Thread.__init__(self)
		self.in_msg = json.loads(in_msg)
		self.start()
		
	def run(self):
		time.sleep(random.randint(0,2))
		conn = open_amqp_conn()
		chan = conn.channel()
		msg = amqp.Message(json.dumps({
			'message_id': self.in_msg['message_id'],
			'body': self.in_msg['body']
		}))
		print 'ping'
		chan.basic_publish(msg, exchange='stupid_client_exchange')

def recv(msg):
	print 'recv'
	chan.basic_ack(msg.delivery_tag)
	print 'received message %s' % msg.body
	RandomRespond(msg.body)
	
chan.basic_consume(
	queue=options.query_queue,
	no_ack=True,
	callback=recv)
	
while True:
	chan.wait()	