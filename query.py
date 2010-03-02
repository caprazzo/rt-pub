from HTTP4Store import HTTP4Store

store = HTTP4Store("http://localhost:8080/")

q = """
	PREFIX dc: <http://purl.org/dc/elements/1.1/>
	PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
	PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
	
	SELECT * WHERE {
		?s <dc:title> ?o .
	} LIMIT 10
"""

r = store.sparql(q)
for r in r:
	print r