# -*- coding: utf-8 -*-
import hashlib
from collections import OrderedDict

__author__ = 'ege'


class UrlHasher:
    """
    helper utility to hash/update/retrieve responding url in a url group
    see: python borg pattern
    """
    __urls = {}
    MAXSIZE = 256

    def __init__(self):
        self.__dict__ = self.__urls
        self.hashes = OrderedDict()

    @staticmethod
    def sort_urls(urls):
        return sorted(urls)

    @staticmethod
    def _hash(urls):
        return hashlib.md5(str(urls)).hexdigest()

    def hashed(self, urls):
        return self._hash(self.sort_urls(urls))

    def hash_urls(self, urls, up):
        if len(self.hashes.keys()) >= self.MAXSIZE:
            self.hashes.popitem(last=False)
        self.hashes.update({self.hashed(urls): up})

    def is_hashed(self, urls):
        return True if self.hashed(urls) in self.hashes.keys() else False

    def master_for(self, urls):
        return self.hashes[self.hashed(urls)]

    def clean_up(self, urls):
        self.hashes.pop(self.hashed(urls))
