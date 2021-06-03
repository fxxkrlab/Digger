from __future__ import division, unicode_literals

import collections
import hashlib
import logging
import numbers
import re
import sys
from itertools import groupby

import numpy as np

basestring = str
unicode = str
long = int

def int_to_bytes(n, length):
    return n.to_bytes(length, 'big')

def bytes_to_int(b):
    return int.from_bytes(b, 'big')


def _hashfunc(x):
    return hashlib.md5(x).digest()


class Simhash(object):
    large_weight_cutoff = 50
    batch_size = 200

    def __init__(
            self, value, f=64, reg=r'[\w\u4e00-\u9fcc]+', hashfunc=_hashfunc, log=None
    ):

        if f % 8:
            raise ValueError('f must be a multiple of 8')

        self.f = f
        self.f_bytes = f // 8
        self.reg = reg
        self.value = None
        self.hashfunc = hashfunc
        self.hashfunc_returns_int = isinstance(hashfunc(b"test"), numbers.Integral)

        if log is None:
            self.log = logging.getLogger("simhash")
        else:
            self.log = log

        if isinstance(value, Simhash):
            self.value = value.value
        elif isinstance(value, basestring):
            self.build_by_text(unicode(value))
        elif isinstance(value, collections.Iterable):
            self.build_by_features(value)
        elif isinstance(value, numbers.Integral):
            self.value = value
        else:
            raise Exception('Bad parameter with type {}'.format(type(value)))

    def __eq__(self, other):

        return self.value == other.value

    def _slide(self, content, width=4):
        return [content[i:i + width] for i in range(max(len(content) - width + 1, 1))]

    def _tokenize(self, content):
        content = content.lower()
        content = ''.join(re.findall(self.reg, content))
        ans = self._slide(content)
        return ans

    def build_by_text(self, content):
        features = self._tokenize(content)
        features = {k:sum(1 for _ in g) for k, g in groupby(sorted(features))}
        return self.build_by_features(features)

    def build_by_features(self, features):

        sums = []
        batch = []
        count = 0
        w = 1
        truncate_mask = 2 ** self.f - 1
        if isinstance(features, dict):
            features = features.items()

        for f in features:
            skip_batch = False
            if not isinstance(f, basestring):
                f, w = f
                skip_batch = w > self.large_weight_cutoff or not isinstance(w, int)

            count += w
            if self.hashfunc_returns_int:
                h = int_to_bytes(self.hashfunc(f.encode('utf-8')) & truncate_mask, self.f_bytes)
            else:
                h = self.hashfunc(f.encode('utf-8'))[-self.f_bytes:]

            if skip_batch:
                sums.append(self._bitarray_from_bytes(h) * w)
            else:
                batch.append(h * w)
                if len(batch) >= self.batch_size:
                    sums.append(self._sum_hashes(batch))
                    batch = []

            if len(sums) >= self.batch_size:
                sums = [np.sum(sums, 0)]

        if batch:
            sums.append(self._sum_hashes(batch))

        combined_sums = np.sum(sums, 0)
        self.value = bytes_to_int(np.packbits(combined_sums > count / 2).tobytes())

    def _sum_hashes(self, digests):
        bitarray = self._bitarray_from_bytes(b''.join(digests))
        rows = np.reshape(bitarray, (-1, self.f))
        return np.sum(rows, 0)

    @staticmethod
    def _bitarray_from_bytes(b):
        return np.unpackbits(np.frombuffer(b, dtype='>B'))

    def distance(self, another):
        assert self.f == another.f
        x = (self.value ^ another.value) & ((1 << self.f) - 1)
        ans = 0
        while x:
            ans += 1
            x &= x - 1
        return ans