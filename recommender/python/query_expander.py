import tornado
import tornado.ioloop
import tornado.httpclient
from tornado.options import options

import threading
import time
from amqplib import client_0_8 as amqp
import simplejson as json
from system_conf import open_amqp_conn
#tornado.options.parse_config_file('system_conf.py')
tornado.options.parse_command_line()
import logging
log = logging.getLogger(__name__)

class QueueSender(threading.Thread):
	
	def __init__(self, open_amqp_conn, exchange):
		log.info('Init queue sender on exchange [%s]' % exchange)
		threading.Thread.__init__(self)
		self.open_amqp_conn = open_amqp_conn
		self.exchange = exchange
		self.do_stop = False
		self.messages = []
		self.flushing = False
		self.chan = None
		
	def run(self):
		conn = self.open_amqp_conn()
		self.chan = conn.channel()
		log.info('Start sender on exchange [%s]' % self.exchange)
		while not self.do_stop:
			if not self.flushing:
				self._flush()
			time.sleep(0.001)
		self.chan.close()
		conn.close()
	
	def send(self, obj):
		self.messages.append(obj)
		
	def _flush(self):
		self.flushing = True
		while len(self.messages) > 0:
			self._send(self.messages.pop())
		self.flushing = False
	
	def _send(self, obj):
		body = json.dumps(obj)
		msg = amqp.Message(body)
		msg.properties["delivery_mode"] = 1
		log.info('publishing request [%s]' % body)
		self.chan.basic_publish(msg, exchange=self.exchange)
		
	def stop(self):
		log.info('Stopping queue sender on exchange [%s]' % self.exchange)
		self.do_stop = True
		
class QueueListener(threading.Thread):

	def __init__(self, open_amqp_conn, queue):
		log.info('Init queue listener on queue [%s]' % queue)
		threading.Thread.__init__(self)
		self.open_amqp_conn = open_amqp_conn
		self.queue = queue
		self.do_stop = False
		self.chan = None
		self.callback = None
		
	def recv(self, msg):
		log.info('Received message [%s]' % msg)
		print dir(msg)
		print msg.body
		self.callback(msg)
		self.chan.basic_ack(msg.delivery_tag)
			
	def onMessage(self, callback):
		self.callback = callback

	def run(self):
		conn = self.open_amqp_conn()
		self.chan = conn.channel()
		log.info('Start consuming queue %s' % self.queue)	
		try:
			self.chan.basic_consume(queue=self.queue, no_ack=False, callback=self.recv)
			while not self.do_stop:
				self.chan.wait()
		except Exception, e:
			log.error('Exception [%s]', str(e))
		log.info('Stopping')
		self.chan.close()
		conn.close()

	def stop(self):
		log.info("Stopping queue listener on [%s]" % self.queue)
		self.do_stop = True
		
def amqp_respond(queue_sender, message_id, profiles):
	env = {
		'message_id': message_id,
		'body': {
			'web_query': profiles
		}
	}
	queue_sender.send(env)

def main():
	ql = QueueListener(open_amqp_conn, 'initial_query_queue')
	qs = QueueSender(open_amqp_conn, 'query_exchange')
	try:
		def amqp_recv(message):
			log.info('amqp_recv seeing message %s' % message.body)
			obj = json.loads(message.body)
			message_id = obj['message_id']
			profile = obj['body']['web_query']
			url = '%s/otherme?q=%s' % (options.social_graph_api_url, profile)
						
			def http_recv(response):
				log.info('response from graph api: %s' % response.body)
				social_graph = json.loads(response.body)
				
				others = social_graph.keys()
				others.append(profile)
				amqp_respond(qs,message_id, others)
				
			http = tornado.httpclient.AsyncHTTPClient()	
			http.fetch(url, http_recv)			
			
		ql.onMessage(amqp_recv)
		ql.start()
		qs.start()	
		tornado.ioloop.IOLoop.instance().start()
	except:
		qs.stop()		
		ql.stop()
		qs.join()
		ql.join()
		tornado.ioloop.IOLoop.instance().stop()
	
if __name__ == "__main__":
	main()