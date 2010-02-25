import httplib
def get(host,port,url):
    h = httplib.HTTP(host, port)
    h.putrequest('GET', url)
    h.putheader('Host', host)
    h.putheader('User-agent', 'python-httplib')
    h.endheaders()

    (returncode, returnmsg, headers) = h.getreply()
    if returncode != 200:
        print returncode, returnmsg
        sys.exit()

    f = h.getfile()
    print f.read()
    

def get2():
	import httplib
	conn = httplib.HTTPConnection("localhost:8888")
	conn.request("GET", "/")
	r1 = conn.getresponse()
	print r1.status, r1.reason
	
	for l in r1.read(100):
		print l

def get3():
	import urllib
	
	req = urllib.urlopen('http://localhost:8888/')    
	for dat in req: 
	    print dat
	    
get3()