import shlex, subprocess
import threading, time
import json

class Fetch(threading.Thread):
	
	def __init__(self, num):
		threading.Thread.__init__(self)
		self.num = num
		self.start()
		
	def run(self):
		command_line = 'curl -s http://localhost:8888/search?q=%s' % self.num
		args = shlex.split(command_line)
		p = subprocess.Popen(args, bufsize=1, stdout=subprocess.PIPE)
		rx = p.stdout.read().split('Received').pop().strip()
		try:
			resp = int(json.loads(rx)['body']['web-query'][1])
			print 'request %d --> %d\n' % (self.num, resp)
			if resp is not self.num:
				print '%s != %s' % (resp, self.num)
		except ValueError:
			print rx

for num in range(100):
	Fetch(num)
	