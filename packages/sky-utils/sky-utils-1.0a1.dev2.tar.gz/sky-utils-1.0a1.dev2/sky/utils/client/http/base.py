# -*- coding: utf-8 -*-
import json
import httplib2

__author__ = 'ahmetdal'


class HttpClient(object):

    @classmethod
    def get_connection(cls, timeout=None):
        return httplib2.Http(timeout=timeout)

    @classmethod
    def get_connection_ignore_ssl(cls, timeout=None):
        return httplib2.Http(disable_ssl_certificate_validation=True, timeout=timeout)

    @classmethod
    def get(cls, uri, headers=None, ignore_ssl=False, timeout=None):
        return HttpClient.__request(uri, "GET", None, headers=headers, ignore_ssl=ignore_ssl, timeout=timeout)

    @classmethod
    def post(cls, uri, data=json.dumps({}), headers=None, ignore_ssl=False, timeout=None):
        return HttpClient.__request(uri, "POST", data, headers=headers, ignore_ssl=ignore_ssl, timeout=timeout)

    @classmethod
    def put(cls, uri, data=json.dumps({}), headers=None, ignore_ssl=False, timeout=None):
        return HttpClient.__request(uri, "PUT", data, headers=headers, ignore_ssl=ignore_ssl, timeout=timeout)

    @classmethod
    def delete(cls, uri, headers=None, ignore_ssl=False, timeout=None):
        return HttpClient.__request(uri, "DELETE", None, headers=headers, ignore_ssl=ignore_ssl, timeout=timeout)

    @classmethod
    def proxy(cls, url, method, data=None, headers=None, ignore_ssl=False):
        return HttpClient.__request(url, method, data, headers, ignore_ssl=ignore_ssl)

    @classmethod
    def __request(cls, url, method, data=None, headers=None, ignore_ssl=False, timeout=None):
        if not isinstance(data, basestring):
            data = json.dumps(data) if data is not None else data
        if ignore_ssl:
            return HttpClient.get_connection_ignore_ssl(timeout=timeout).request(url, method, body=data, headers=headers)
        else:
            return HttpClient.get_connection(timeout=timeout).request(url, method, body=data, headers=headers)
