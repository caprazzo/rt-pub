from xml.dom import minidom
from reader import Reader
import logging
import logging.config

from time import time
import rdflib
import sys

users_file = sys.argv[1]
items_file = sys.argv[2]
out_dir = sys.argv[3]
session = time()
logging.config.fileConfig('logging.conf')
log = logging.getLogger('complete_items_%s' % str(session))

def parse(item_dom):
	item = {'id':None, 'title':None, 'link':None, 'categories':[]}
	for element in item_dom.childNodes:
		if element.localName == 'id' and element.firstChild and element.firstChild.data:
			item['id'] = element.firstChild.data.split('/').pop()
		elif element.localName == 'title' and element.firstChild and element.firstChild.data:
			item['title'] = element.firstChild.data
		elif element.localName == 'link' and element.hasAttribute('rel') and element.getAttribute('rel') == 'alternate':
			item['link'] = element.getAttribute('href')
		elif element.localName == 'category' and element.hasAttribute('term'):
			item['categories'].append(element.getAttribute('term').strip())
	return item
	
def item_uri(item_id):
	return rdflib.URIRef('http://www.google.com/reader/item/' + item_id)


from slist import Slist

def load(users_file, items_file):
	wanted_items = Slist()
	for item_id in open(items_file):
		wanted_items.append(item_id.rstrip())
	log.info('loaded %d items' % len(wanted_items))

	users = []
	for user_id in open(users_file):
		users.append(user_id.rstrip().split(' '))
	log.info('loaded %d users' % len(users))
	
	return (wanted_items, users)


log.info('start')

r = Reader()	
count = 0
wanted_items, users = load(users_file, items_file)

dc = rdflib.Namespace('http://purl.org/dc/elements/1.1/')
cu = rdflib.Namespace('http://caprazzi.net/cu/2010/')
cat = rdflib.Namespace('http://caprazzi.net/cat/2010/')
rdf = rdflib.Namespace('http://www.w3.org/1999/02/22-rdf-syntax-ns#')
foaf = rdflib.Namespace('http://xmlns.com/foaf/0.1/')
atom = rdflib.Namespace('http://www.w3.org/2005/Atom/')

def graph():
	g = rdflib.ConjunctiveGraph()
	g.bind('dc', dc)
	g.bind('cu', cu)
	g.bind('foaf', foaf)
	g.bind('atom', atom)
	g.bind('cat', cat)
	return g

def store(s, o, p):
	g.add((s, o, p))
	
def store_item(item):
	uri = item_uri(item['id'])
	
	if item['link'] is not None:
		store(uri, dc['source'], rdflib.URIRef(item['link']))
		
	if item['title'] is not None:
		store(uri, dc['title'], rdflib.Literal(unicode(item['title'])))
		
	for category in item['categories']:
		store(uri, atom['category'], cat[category.lower()])
		

flush_count = 0
progress_count = 0
def flush(g, out_dir, flush_count):
	dest = '%s/flush-%d-%04d.rdf' % (out_dir, session, flush_count)
	log.info('flushing %d triples to %s' % (len(g), dest))	
	g.serialize(destination=dest, format='xml')

g = graph()
try:
	while len(wanted_items) > 0 and len(users) > 0:
		user_id, share_count = users.pop()
		log.info('getting user %s, %s items' % (user_id, share_count))
		for item_dom in r.shared_items(user_id, page_size=300, max=int(share_count)):
			item = parse(item_dom)
			if wanted_items.try_remove(item['id']):
				store_item(item)
				progress_count += 1
				
			if progress_count > 100:
				log.info('graph size %d' % len(g))
				progress_count = 0
				
			if len(g) >= 10000:
				flush(g, out_dir, flush_count)
				del g
				g = graph()
				flush_count += 1
			
		log.info('done user %d of %d, %d items to go' % (count, len(users), len(wanted_items)))
		count += 1
		
except Exception, e:
	print e
	log.info('exception %s' % e)
	flush(g, out_dir, 99999)
	exit(1)