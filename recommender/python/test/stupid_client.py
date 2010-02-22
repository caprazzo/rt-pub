# brutal hack to access modules from parent dir
import sys
sys.path.insert(0, '..')

from amqplib import client_0_8 as amqp
import tornado
from tornado.options import options
from system_conf import open_amqp_conn

tornado.options.parse_command_line()
import simplejson as json

conn = open_amqp_conn()
	
chan = conn.channel()
chan.exchange_declare(exchange='stupid_client_exchange', type="fanout")
chan.queue_bind(queue='response_queue', exchange='stupid_client_exchange')
	
def recv(msg):
	chan.basic_ack(msg.delivery_tag)
	print 'received message %s' % msg.body
	obj = json.loads(msg.body)
	input = raw_input("your answer? ")
	envelope = {
		'message_id': obj['message_id'],
		'body': input
	}
	print 'sending %s' % envelope
	msg = amqp.Message(json.dumps(envelope))
	msg.properties["delivery_mode"] = 2
	chan.basic_publish(msg, exchange='stupid_client_exchange')
	
chan.basic_consume(
	queue=options.query_queue,
	no_ack=True,
	callback=recv)
	
while True:
	chan.wait()	