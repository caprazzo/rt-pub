#!/usr/bin/python
# -*- coding: utf-8 -*-

import httplib2
from urllib import urlencode

from sparql_response import SparqlResponseHandler

from utils import RequestHandler

from xml.etree import ElementTree as ET

mapping_type = {'turtle':'application/x-turtle',
                'xml':'application/rdf+xml',
                'n3':'text/rdf+n3',
                'nt':'text/rdf+nt',
                'trig':'application/x-trig',
                }

class HTTP4Store(object):
    def __init__(self, http_endpoint="http://localhost:5000/"):
        if not http_endpoint.endswith('/'):
            http_endpoint = "%s/" % http_endpoint
        self.http_endpoint = http_endpoint
        self.sparql_endpoint = "%ssparql/" % http_endpoint
        self.data_endpoint = "%sdata/" % http_endpoint
        self.status_endpoint = "%sstatus/" % http_endpoint
        self.rh = RequestHandler()
        self.sh = SparqlResponseHandler()

    def status(self):
        robj = self.rh.GET(self.status_endpoint)
        assert robj.status == 200
        status = {}
        # Chop off the crud at the top
        doc = ET.fromstring(robj.content.split('\n', 1)[-1])
        body = doc.find('body')
        for row in body.find('table').findall('tr'):
            l,r = row.getchildren()
            if l.text == "Running queries":
                status['running'] = int(r.text)
            elif l.text == "Outstanding queries":
                status['outstanding'] = int(r.text)
        status['kb'] = body.find('h2').text[3:]
        return status
    
    def sparql(self, query_string, accept="text/tab-separated-values", headers={}, get_raw_response_obj=False):
        print 'CAZZI'
        if accept:
            headers['Accept'] = accept
        resp_obj = self.rh.GET(self.sparql_endpoint, headers=headers, query=query_string)
        if get_raw_response_obj:
            return resp_obj
        return self.sh.parse(resp_obj)
        
    def add_from_uri(self, uri, accept="application/rdf+xml", headers={}):
        if accept:
            headers['Accept'] = accept
        r_obj = self.rh.GET(uri, headers=headers)
        assert r_obj.status == 200
        return self.add_graph(uri, r_obj.content, content_type=r_obj.content_type)

    def add_graph(self, uri, content, content_type="turtle"):
        """content_type := turtle|xml|nt|n3|trig
            turtle, rdf/xml, ntriples, N3, and TriG respectively"""
        
        headers = {}
        headers['content-type'] = mapping_type.get(content_type, content_type)
        
        # TODO - if content is a graph -> serialised form for posting
        
        return self.rh.PUT("%s%s" % (self.sparql_endpoint, uri), 
                               headers=headers, 
                               body=content)
    
    def append_graph(self, uri, content, content_type="turtle"):
        """content_type := turtle|xml|nt|n3|trig
            turtle, rdf/xml, ntriples, N3, and TriG respectively"""
        
        headers = {}
        headers['content-type'] = mapping_type.get(content_type, 'application/x-turtle')
        
        # TODO - if content is a graph -> serialised form for posting
        
        params = {}
        params['graph'] = uri
        params['data'] = content
        params['mime-type'] = headers['content-type']
        
        resp_obj = self.rh.POST(self.data_endpoint,
                               headers=headers, 
                               body=urlencode(params)
                               )
        return resp_obj
    
    def del_graph(self, uri):
        resp_obj = self.rh.DELETE( "%s%s" % (self.sparql_endpoint, uri) )
        assert resp_obj.status == 200
        return resp_obj

