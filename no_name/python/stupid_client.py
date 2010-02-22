from amqplib import client_0_8 as amqp
import tornado
from tornado.options import options
tornado.options.parse_config_file('system_conf.py')
tornado.options.parse_command_line()
import simplejson as json
conn = amqp.Connection(
	host=options.amqp_host,
	userid="guest", 
	password="guest",
	virtual_host="/",
	insist=False)
	
chan = conn.channel()

chan.queue_declare(
	queue=options.response_queue,
	durable=True,
	exclusive=False,
	auto_delete=False)
	
chan.queue_declare(
	queue=options.query_queue,
	durable=True,
	exclusive=False,
	auto_delete=False)
	
chan.exchange_declare(
	exchange='stupid_client_exchange',
	type="fanout",
	durable=True,
	auto_delete=False)
	
chan.queue_bind(
	queue=options.response_queue,
	exchange='stupid_client_exchange')
	
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
	
	