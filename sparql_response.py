#!/usr/bin/python
# -*- coding: utf-8 -*-

import rdflib
from rdflib import URIRef, Literal
from rdflib import ConjunctiveGraph as CG

# For the from text parse of rdflib graph 2.4.2:
from xml.sax.xmlreader import InputSource

from xml.etree import ElementTree as ET

import simplejson

from StringIO import StringIO

class SparqlResponseHandler(object):
    def __init__(self, response_object=None):
        if response_object:
            self.parse(response_object)
    def parse(self, r):
        # define some nested helper functions
        def _xml_list_parse(response_object):
            sparql_ns = "{http://www.w3.org/2005/sparql-results#}%s"
            sparql_vars = []
            sparql_results = []
            try:
                content = response_object.content
                if response_object.charset:
                    content = response_object.content.decode(response_object.charset)
            
                etree = ET.fromstring(content)
                """
                # Not needed so commented, but included for completeness
                head = etree.find(sparql_ns % "head")
                for variable in head.getchildren():
                    name = variable.get('name')
                    if name:
                        sparql_vars.append(name)
                    else:
                        raise Exception("not sparql?")
                """
                results = etree.find(sparql_ns % "results")
                for result in results.getchildren():
                    result_d = {}
                    for binding in result.getchildren():
                        var_name = binding.get('name')
                        if var_name.startswith("?"):
                            # should be all of them
                            var_name = var_name[1:]
                        value = binding.getchildren().pop()
                        text = value.text
                        if value.tag == sparql_ns % "uri":
                            result_d[unicode(var_name)] = URIRef(text)
                        else:
                            result_d[unicode(var_name)] = Literal(text)
                    sparql_results.append(result_d)
                return sparql_results
            except:
                raise Exception

        def _tsv_list_parse(response_object):
            sparql_results = []
            content = response_object.content
            if response_object.charset:
                content = response_object.content.decode(response_object.charset)
            
            tsv_list = content.split('\n')
            var_list = []
            for name in tsv_list.pop(0).split('\t'):
                if name.startswith('?'):
                    var_list.append(name[1:])
                else:
                    var_list.append(name)

            for line in tsv_list:
                if line:
                    result_d = {}
                    r_list = line.split('\t')
                    for index in xrange(0,len(var_list)):
                        if r_list[index].startswith('<') and r_list[index].endswith('>'):
                            result_d[var_list[index]] = URIRef(r_list[index][1:-1])
                        else:
                            result_d[var_list[index]] = Literal(r_list[index])
                    sparql_results.append(result_d)
            return sparql_results

        def _graph_parse(response_object):
            class TextInputSource(InputSource, object):
                def __init__(self, text, system_id=None):
                    super(TextInputSource, self).__init__(system_id)
                    self.url = system_id
                    file = StringIO(text)
                    self.setByteStream(file)
                    # TODO: self.setEncoding(encoding)

                def __repr__(self):
                    return self.url
            t = TextInputSource(response_object.content)
            g = CG()
            if response_object.content_type.endswith("n3"):
                g = g.parse(t, format="n3")
            elif response_object.content_type.endswith("turtle"):
                g = g.parse(t, format="turtle")
            elif response_object.content_type.endswith("xml"):
                g = g.parse(t, format="xml")
            return g

        def _json_parse(response_object):
            sparql_results = []
            doc = simplejson.loads(response_object.content)
            for result in doc['results']['bindings']:                
                result_d = {}
                for key in result:
                    if result[key]['type'] == 'uri':
                        result_d[key] = URIRef(result[key]['value'])
                    else:
                        result_d[key] = Literal(result[key]['value'])
                sparql_results.append(result_d)
            return sparql_results
#            return simplejson.loads(response_object.content)

        # Check response type:
        if r.status in [200,204]:
            if r.content_type.endswith('json'):
                return _json_parse(r)
            elif r.content_type.endswith("xml"):
                return _xml_list_parse(r)
            elif r.content_type.startswith("text/tab-separated-values"):
                return _tsv_list_parse(r)
            elif r.content_type.startswith("text/rdf+n3"):
                return _graph_parse(r)
        elif r.status >= 500:
            raise Exception("Error %s - %s" % (r.status, r.resp.reason))
        elif r.status == 404:
            raise Exception("Error 404 - %s" % (r.resp.reason))

