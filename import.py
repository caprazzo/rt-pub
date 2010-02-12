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

f = open('store_sample.txt')
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
		g.add((item, rdf.type, Literal("google reader item")))

g.commit()
print g.serialize(format='n3')
#05429296530037195610