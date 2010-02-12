import rdflib
from rdflib.Graph import ConjunctiveGraph as Graph
from rdflib import plugin
from rdflib.store import Store, NO_STORE, VALID_STORE
from rdflib import Namespace
from rdflib import Literal
from rdflib import URIRef

default_graph_uri = "http://rdflib.net/rdfstore"
configString = "host=localhost,user=username,password=password,db=rdfstore"

# Get the mysql plugin. You may have to install the python mysql libraries
store = plugin.get('SQLite', Store)('rdfstore.ts')

# Open previously created store, or create it if it doesn't exist yet
rt = store.open('.',create=True)
if rt == NO_STORE:
    # There is no underlying MySQL infrastructure, create it
    store.open(configString,create=True)
else:
    assert rt == VALID_STORE,"There underlying store is corrupted"
    
# There is a store, use it
graph = Graph(store, identifier = URIRef(default_graph_uri))

print "Triples in graph before add: ", len(graph)

# Now we'll add some triples to the graph & commit the changes
rdflib = Namespace('http://rdflib.net/test/')
graph.add((rdflib['pic:1'], rdflib['name'], Literal('Jane & Bob')))
graph.add((rdflib['pic:2'], rdflib['name'], Literal('Squirrel in Tree')))
graph.commit()

print "Triples in graph after add: ", len(graph)

# display the graph in RDF/XML
print graph.serialize()