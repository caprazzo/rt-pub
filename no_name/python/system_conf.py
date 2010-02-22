from tornado.options import define
from tornado.options import options
from amqplib import client_0_8 as amqp

define('social_graph_api_url', default='http://socialgraph.apis.google.com',
	help="social graph api endpoint", type=str)
	
# web service conf
define('web_server_port', default=8888,
	help="run on the given port", type=int)   

define('web_query_timeout', default=10, 
	help="maximum time client waits for an answer, in seconds", type=int)

define('web_query_exchange', default='query_exchange',
	help='name of the exchange where web queries are published')
	
# queue conf and setup
define('amqp_host', default='localhost:5672',
	help="connect to this amqp server", type=str)

define('query_queue', default='query_queue',
	help='name of the queue that distributes new queries', type=str)

define('response_queue', default='response_queue',
	help='name of the queue that distributes complete answers', type=str)
	


conn = amqp.Connection(host=options.amqp_host,
	userid="guest", password="guest",
	virtual_host="/", insist=False)
chan = conn.channel()

# web_server ---[initial_query_queue]---> query_expander
chan.queue_declare(queue='initial_query_queue',
	durable=False, exclusive=False,  auto_delete=True)
chan.exchange_declare(exchange='initial_query_exchange',
	type="fanout", durable=False, auto_delete=True)
chan.queue_bind(queue='initial_query_queue', 
	exchange='initial_query_exchange')

# query_expander ---[query_queue]---> recommender
chan.queue_declare(queue='query_queue',
	durable=False, exclusive=False,  auto_delete=True)
chan.exchange_declare(exchange='query_exchange',
	type="fanout", durable=False, auto_delete=True)
chan.queue_bind(queue='query_queue',
	exchange='query_exchange')

# recommender ---[response_queue]---> web_server	
chan.queue_declare(queue='response_queue',
	durable=False, exclusive=False,  auto_delete=True)
chan.exchange_declare(exchange='response_exchange',
	type="fanout", durable=False, auto_delete=True)
chan.queue_bind(queue='response_queue',
	exchange='response_exchange')

chan.close()
conn.close()

def open_amqp_conn():
	return amqp.Connection(host=options.amqp_host,
		userid="guest", password="guest",
		virtual_host="/", insist=False)