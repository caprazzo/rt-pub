import rdflib
from rdflib import Literal
from rdflib import BNode
import sys
offset = int(sys.argv[1])
store = rdflib.plugin.get('SQLite', rdflib.store.Store)('import-test.2.bak')
store.open('.', create=False)


g = rdflib.ConjunctiveGraph(store)

#dc = rdflib.Namespace('http://purl.org/dc/elements/1.1/')
#cu = rdflib.Namespace('http://caprazzi.net/cu/2010/')
#rdf = rdflib.Namespace('http://www.w3.org/1999/02/22-rdf-syntax-ns#')
#foaf = rdflib.Namespace('http://xmlns.com/foaf/0.1/')

#item = rdflib.Namespace('')

#g.bind('dc', dc)
#g.bind('cu', cu)
#g.bind('item',item)
#g.bind('foaf', foaf)

print len(g)