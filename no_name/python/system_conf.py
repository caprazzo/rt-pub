from tornado.options import define

# system conf
define('amqp_host', default='localhost:5672',
	help="connect to this amqp server", type=str)
	
define('query_queue', default='query_queue',
	help='name of the queue that distributes new queries', type=str)
	
define('response_queue', default='response_queue',
	help='name of the queue that distributes complete answers', type=str)

# web service conf
define('web_server_port', default=8888,
	help="run on the given port", type=int)   
	
define('web_query_exchange', default='query_exchange',
	help='name of the exchange where web queries are published')
