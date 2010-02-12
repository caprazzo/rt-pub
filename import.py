try: import json
except: import simplejson as json
import rdflib
from rdflib import Literal
from rdflib import BNode
def item_id(item):
	return item.split('/').pop()




store = rdflib.plugin.get('Memory', rdflib.store.Store)('')
g = rdflib.ConjunctiveGraph()

dc = rdflib.Namespace('http://purl.org/dc/elements/1.1/')
cu = rdflib.Namespace('http://caprazzi.net/cu/2010/')
rdf = rdflib.Namespace('http://www.w3.org/1999/02/22-rdf-syntax-ns#')
foaf = rdflib.Namespace('http://xmlns.com/foaf/0.1/')

item = rdflib.Namespace('')

g.bind('dc', dc)
g.bind('cu', cu)
g.bind('item',item)
g.bind('foaf', foaf)

#f = open('store_sample.txt','r')
f = open('/cygdrive/e/store.txt','r')
reader_item = Literal("google reader item")
count = 0
for line in f:
	
	subj, pred, obj = json.loads(line)
	
	if pred == 'cu:likes':
		p = BNode(subj)
		g.add((p, cu.likes, BNode(obj)))
		g.add((p, rdf.type, foaf.person))
		g.add((p, foaf.account, rdflib.URIRef('http://www.google.com/reader/shared/'+subj)))
		
	elif pred == 'cu:shares':
		p = BNode(subj)
		g.add((p, cu.shares, BNode(obj)))
		g.add((p, rdf.type, foaf.person))
		g.add((p, foaf.account, rdflib.URIRef('http://www.google.com/reader/shared/'+subj)))
	
	elif pred == 'dc:title':
		item = BNode(subj)
		g.add((item, dc['title'], Literal(obj)))
		g.add((item, rdf.type, reader_item))
	
	g.commit()
	if count >= 5000:
		break
	if count % 1000 == 0:
		print count, len(g)
	count += 1
	

f.close()
g.serialize(destination='store.rdf', format='xml')
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