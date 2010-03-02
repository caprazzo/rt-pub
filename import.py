try: import json
except: import simplejson as json
import rdflib
from rdflib import Literal
from rdflib import BNode
import sys

def item_id(item):
	return item.split('/').pop()
offset = int(sys.argv[1])
#store = rdflib.plugin.get('SQLite', rdflib.store.Store)('import-test.%s.ts' % offset)
#store.open('.', create=True)


g = rdflib.ConjunctiveGraph()

dc = rdflib.Namespace('http://purl.org/dc/elements/1.1/')
cu = rdflib.Namespace('http://caprazzi.net/cu/2010/')
rdf = rdflib.Namespace('http://www.w3.org/1999/02/22-rdf-syntax-ns#')
foaf = rdflib.Namespace('http://xmlns.com/foaf/0.1/')
atom = rdflib.Namespace('')

item = rdflib.Namespace('')

g.bind('dc', dc)
g.bind('cu', cu)
g.bind('item',item)
g.bind('foaf', foaf)


step=3
def item_uri(id):
	return rdflib.URIRef('http://www.google.com/reader/item/' + id.split('/').pop())
#f = open('store_sample.txt','r')
f = open('store.txt','r')
reader_item = Literal("google reader item")
count = 0
import datetime
start = datetime.datetime.now()
chunk = start
rdf_chunk_size = 100000
for line in f:
	
	subj, pred, obj = json.loads(line)

	if pred == 'cu:likes':
		#p = BNode(subj)
		g.add((rdflib.URIRef('http://www.google.com/reader/shared/'+subj), cu.likes, item_uri(obj)))
		#g.add((p, rdf.type, foaf.person))
		#g.add((p, foaf.account, rdflib.URIRef('http://www.google.com/reader/shared/'+subj)))
	
	elif pred == 'cu:shares':
		#p = BNode(subj)
		g.add((rdflib.URIRef('http://www.google.com/reader/shared/'+subj), cu.shares, item_uri(obj)))
		#g.add((p, rdf.type, foaf.person))
		#g.add((p, foaf.account, rdflib.URIRef('http://www.google.com/reader/shared/'+subj)))

	elif pred == 'dc:title':
		#item = BNode(subj)
		g.add((item_id(subj), dc['title'], Literal(obj)))
		#g.add((item, rdf.type, reader_item))
	else:
		print 'unknown pred [%s]' % pred
		
		
	#if count % 10000 == 0:
	#	g.commit()
	
	#if count >= 5000:
	#	break
	
	if count % 10000 == 0:
		print str(datetime.datetime.now() - start), str(datetime.datetime.now() - chunk), count, len(g)
		chunk = datetime.datetime.now()
		
	
	if count > 0 and count % rdf_chunk_size == 0:

		dest = 'rdf/store-%s-%04d.rdf' % (rdf_chunk_size, (count / rdf_chunk_size))
		print 'flushing to %s' % dest
		g.serialize(destination=dest, format='xml')
		g = rdflib.ConjunctiveGraph()

	
	count += 1
	
dest = 'rdf/store-%s-%04d.rdf' % (rdf_chunk_size, 999)
print 'flushing to %s' % dest
g.serialize(destination=dest, format='xml')

#g.commit()
print str(datetime.datetime.now() - start)

f.close()
#g.serialize(destination='store.rdf', format='xml')
#results = g.query("""SELECT ?user ?item
#			WHERE { ?user cu:likes ?item . } """, initNs={'cu':cu, 'dc':dc})
			
#import networkx as nx


#ng = nx.Graph()
#for triple in results:
#	print triple[0], triple[1].split('/').pop()
#	ng.add_edge(str(triple[0]), str(triple[1]).split('/').pop())
	
#rt = nx.betweenness_centrality(ng)
#for v in rt:
#	print v, rt[v]
	
#for t in nx.find_cliques(ng):
#	print t

#print nx.degree(ng)
#print g.serialize(format='n3')
#05429296530037195610