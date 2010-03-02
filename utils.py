#!/usr/bin/python
# -*- coding: utf-8 -*-

import httplib2
from urllib import urlencode

# For error catching
from socket import error as SocketError

class ResponseObject(object):
    def __init__(self, resp, content):
        self.content = content
        self.status = resp.status
        keys = resp.keys()
        keys.remove('status')
        content_type = ""
        if resp.has_key("Content-Type"):
            content_type = resp["Content-Type"]
            keys.remove('Content-Type')
        elif resp.has_key("content-type"):
            # There's probably a simpler way to deal with this,
            # but I'll leave this as a # TODO
            content_type = resp["content-type"] 
            keys.remove('content-type')
        if content_type:
            if len(content_type.split(";")) > 1:
                self.content_type, charset = content_type.split(";")
                self.charset = charset.split('=')[-1]
            else:
                self.content_type = content_type
                # Assuming UTF-8
                self.charset = 'utf-8'
        h = {}
        for key in keys:
            h[key] = resp[key]
        self.headers = h
    
class RequestHandler(object):
    def __init__(self, httplib_connection=None):
        self.h = httplib_connection
        if not self.h:
            self.h = httplib2.Http('.cache')  
    
    def GET(self, path, headers={}, **params):
        data = ""
        if len(params):
            data = urlencode(params)
            return self._request("%s?%s" % (path, data), method="GET", headers=headers)
        else:
            return self._request("%s" % (path), method="GET", headers=headers)

    def PUT(self, path, headers={}, body=None, **params):
        data = ""
        if len(params):
            data = urlencode(params)
            return self._request(path, method="PUT", headers=headers, data=data)
        elif body:
            return self._request(path, method="PUT", headers=headers, data=body) 
        else:
            return self._request(path, method="PUT", headers=headers)                
            
    def POST(self, path, headers={}, body=None, **params):
        data = ""
        if len(params):
            data = urlencode(params)
            return self._request(path, method="POST", headers=headers, data=data)
        elif body:
            return self._request(path, method="POST", headers=headers, data=body) 
        else:
            return self._request(path, method="POST", headers=headers)            
        
    def DELETE(self, path, headers={}, **params):
        data = ""
        if len(params):
            data = urlencode(params)
            return self._request(path, method="DELETE", headers=headers, data=data)
        else:
            return self._request(path, method="DELETE", headers=headers)
    
    def _request(self, path, method, headers={}, data=None):
        if method not in ["GET", "POST", "PUT", "DELETE"]:
            method = "GET"
        else:
            method = method.upper()

        try:
            # DEBUG
            # print path, method, headers, data
            resp, content = self.h.request(path, method, headers=headers, body=data)
            return ResponseObject(resp, content)
        except SocketError:
            raise Exception("Connection Refused")

