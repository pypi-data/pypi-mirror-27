# -*- coding: utf-8 -*-


import time
import logging
import requests

from json import dumps
from dotmap import DotMap


def debug_request(name, resp, start):
    logger = logging.getLogger(name)

    command = "curl -X {method} -H {headers} -d '{data}' '{uri}'"
    req = resp.request
    method = req.method
    uri = req.url
    data = req.body
    headers = ['"{0}: {1}"'.format(k, v) for k, v in req.headers.items()]
    headers = " -H ".join(headers)
    curl_info = command.format(method=method, headers=headers, data=data or '', uri=uri)
    spent = (time.time() - start) * 1000
    log = logger.error
    content = resp.content
    if resp.status_code >= 200 and resp.status_code < 300:
        log = logger.info
        content = ""
    log("request [{}] spent [{}]ms status [{} - {}] content [[{}]]".format(curl_info, spent, resp.status_code, resp.reason, content))


class Client(object):

    def __init__(self):
        self._sess = requests.Session()

    def do(self, method, url, params=None, data=None, headers=None,
           timeout=20, cert=None, verify=True, files=None, *args, **kwargs):
        req = requests.Request(method, url, params=params, data=data, files=files, headers=headers)
        prepped = req.prepare()
        start = time.time()
        resp = self._sess.send(prepped, verify=verify, cert=cert, timeout=timeout)
        debug_request(__name__, resp, start)
        return resp

    def get(self, url, *args, **kwargs):
        return self.do("GET", url, *args, **kwargs)

    def post(self, url, *args, **kwargs):
        return self.do("POST", url, *args, **kwargs)

    def json(self, url, *args, **kwargs):
        return self.do("POST", url, *args, **kwargs)


class Response(object):

    def __init__(self, resp):
        self._resp = resp

    def json(self):
        return self._resp.json()

    def dotmap(self):
        return DotMap(self._resp.json())

    @property
    def content(self):
        return self._resp.content

    @property
    def status_code(self):
        return self._resp.status_code

    @property
    def ok(self):
        return self._resp.ok


class Chain(object):
    client = Client()

    def __init__(self, path=''):
        self._path = path

    def __getattr__(self, path):
        return Chain('{}/{}'.format(self._path, path))

    def __call__(self, path):
        return Chain('{}/{}'.format(self._path, path))

    def get(self, *args, **kwargs):
        if 'params' in kwargs:
            data = kwargs.pop('params')
        else:
            data, kwargs = kwargs, dict()
        resp = self.client.get(self._path, *args, params=data, **kwargs)
        return Response(resp)

    def post(self, *args, **kwargs):
        if 'data' in kwargs:
            data = kwargs.pop('data')
        else:
            data, kwargs = kwargs, dict()
        resp = self.client.post(self._path, *args, data=data, **kwargs)
        return Response(resp)

    def json(self, *args, **kwargs):
        if 'data' in kwargs:
            data = kwargs.pop('data')
        else:
            data, kwargs = kwargs, dict()
        data = dumps(data)
        headers = kwargs.pop("headers", dict())
        headers["Content-Type"] = "application/json"
        resp = self.client.json(self._path, *args, data=data, headers=headers, **kwargs)
        return Response(resp)

    def __str__(self):
        return "Chain <{}>".format(self._path)

    __repr__ = __str__
