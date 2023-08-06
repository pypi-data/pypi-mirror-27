# -*- coding: utf-8 -*-

import logging
import threading

from .base import HttpClient
from socket import error as socket_error

from sky.utils.client.http.exc import NotMasterURLError
from sky.utils.client.http.utils import UrlHasher

__author__ = 'ege'

url_hasher = UrlHasher()

_lock = threading.RLock()


class FailOverHttpClient(object):
    """
    wraps fail over functionality around HttpClient (moved from esefpy.common)
    iterates over a list of urls, hashes url list as a lookup key and responding
    url in url groups as value so next time calling the client w/ same url group (list of urls),
    client tries to communicate by using previously set responding url (state) instead of retrying all urls
    unless url is not responding anymore, then retries to decide which url is up and updates state on UrlHasher
    """
    client = HttpClient

    @classmethod
    def get(cls, *args, **kwargs):
        return cls._make_request(method='GET', *args, **kwargs)

    @classmethod
    def post(cls, *args, **kwargs):
        return cls._make_request(method='POST', *args, **kwargs)

    @classmethod
    def put(cls, *args, **kwargs):
        return cls._make_request(method='PUT', *args, **kwargs)

    @classmethod
    def delete(cls, *args, **kwargs):
        return cls._make_request(method='DELETE', *args, **kwargs)

    @classmethod
    def _make_request(cls, urls, method, data=None, headers=None,
                      ignore_ssl=False, fail_over_strategy=None, timeout=None):
        _urls = urls
        with _lock:
            response_tuple = None
            hashed = False

            if url_hasher.is_hashed(urls):
                logging.debug("urls are already hashed. cached url for this url group is %s" %
                              url_hasher.master_for(urls))
                _urls = [url_hasher.master_for(urls)]
                hashed = True

            for url in _urls:
                try:
                    if ignore_ssl:
                        response_tuple = cls.client.get_connection_ignore_ssl(timeout=timeout).request(
                            url, method, body=data,  headers=headers)
                    else:
                        response_tuple = cls.client.get_connection(timeout=timeout).request(
                            url, method, body=data, headers=headers)
                    # some services (as a cluster) responds requests w/o having any transmission issues
                    # one might need to find master/slave state of this group by parsing response/content
                    # passing a ´fail_over_strategy´ function to raise any exce
                    if fail_over_strategy and callable(fail_over_strategy):  # check if failover strat. is func
                        fail_over_strategy(*response_tuple)
                except socket_error as se:
                    cls._clean_retry(hashed, se, url, urls, method, data, headers, ignore_ssl)
                    continue
                except NotMasterURLError as ne:
                    cls._clean_retry(hashed, ne, url, urls, method, data, headers, ignore_ssl)
                    continue
                break  # url is responding break loop so we can tell UrlHasher to update state of the url group

            if not hashed:
                logging.debug("hashing url: %s..." % url)
                url_hasher.hash_urls(urls=urls, up=url)

            return response_tuple

    @classmethod
    def _clean_retry(cls, hashed, err, url, urls, *args):
        if isinstance(err, NotMasterURLError):
            logging.warning('not master: %s' % err.message)
        if hashed:
            logging.debug(
                'looks like url (%s) is not responding or declares it\'s not master [message: %s] '
                'cleaning state for this url '
                'making the same request to all urls (%s) to find out which one is responding' %
                (str(url), err.message, ", ".join(urls),))
            logging.debug("url %s is not responding anymore..." % url)
            url_hasher.clean_up(urls)  # previously saved state needs to be changed
            return cls._make_request(urls, *args)  # retry the request

if __name__ == '__main__':
    # > python -m SimpleHTTPServer 9666, client decides the url NOT returning any socket errors as UP (for localhost)
    res = FailOverHttpClient.get(urls=['http://localhost:9666', 'http://ipinfo.io/ip'])
    print ("1. ", res)
    print ("\n%s\n" % str("-" * 15))

    # > return cached/hashed url/host from UrlHasher
    res = FailOverHttpClient.get(urls=['http://localhost:9666', 'http://ipinfo.io/ip'])
    print ("2. ", res)
    print ("\n%s\n" % str("-" * 15))

    # > kill python simple server, client checks for up/available host in given urls again & updates responding host
    res = FailOverHttpClient.get(urls=['http://localhost:9666', 'http://ipinfo.io/ip'])
    print ("3. ", res)
    print ("\n%s\n" % str("-" * 15))

    # > return cached/hashed url from UrlHasher (for ipinfo)
    res = FailOverHttpClient.get(urls=['http://localhost:9666', 'http://ipinfo.io/ip'])
    print ("4. ", res)
    print ("\n%s\n" % str("-" * 15))

    # results:
    # hashing url: http://localhost:9666...
    # 1.({'status': '200', 'content-length': '714', 'content-location': 'http://localhost:9666',
    #     'server': 'SimpleHTTP/0.6 Python/2.7.12', 'date': 'Mon, 20 Feb 2017 11:06:17 GMT',
    #     'content-type': 'text/html; charset=UTF-8'},
    #    '<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 3.2 Final//EN"><html>\n<title>Directory listing for /</title>\n<bod...
    #
    # ---------------
    #
    # urls are already hashed.
    # cached url for this url group is http://localhost:9666
    # 2.({'status': '200', 'content-length': '714', 'content-location': 'http://localhost:9666',
    #     'server': 'SimpleHTTP/0.6 Python/2.7.12', 'date': 'Mon, 20 Feb 2017 11:06:20 GMT',
    #     'content-type': 'text/html; charset=UTF-8'},
    #    '<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 3.2 Final//EN"><html>\n<title>Directory listing for /</title>\n<bod...
    #
    # ---------------
    #
    # urls are already hashed.
    # cached url for this url group is http://localhost:9666
    # url http://localhost:9666 is not responding anymore...
    # hashing url: http://ipinfo.io/ip...
    # 3.({'status': '200', 'content-length': '14', 'content-location': 'http://ipinfo.io/ip',
    #     'set-cookie': 'first_referrer=; Path=/', 'server': 'nginx/1.8.1', 'connection': 'keep-alive',
    #     'date': 'Mon, 20 Feb 2017 11:06:26 GMT', 'access-control-allow-origin': '*',
    #     'content-type': 'text/html; charset=utf-8'}, '85.97.122.232\n')
    #
    # ---------------
    #
    # urls are already hashed.
    # cached url for this url group is http://ipinfo.io/ip
    # 4.({'status': '200', 'content-length': '14', 'content-location': 'http://ipinfo.io/ip',
    #     'set-cookie': 'first_referrer=; Path=/', 'server': 'nginx/1.8.1', 'connection': 'keep-alive',
    #     'date': 'Mon, 20 Feb 2017 11:06:27 GMT', 'access-control-allow-origin': '*',
    #     'content-type': 'text/html; charset=utf-8'}, '85.97.122.232\n')
    #
    # ---------------
