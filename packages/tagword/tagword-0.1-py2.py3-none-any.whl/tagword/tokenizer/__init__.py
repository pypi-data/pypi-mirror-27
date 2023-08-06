#! /usr/bin/python
# -*- coding:utf-8 -*-

import os

from .basic import BasicTokenizer
from .hmm import HMMTokenizer
from .crfpp import CRFPPTokenizer


class Tokenizer(object):
    def __init__(self, mode='basic'):
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.basictokenizer = BasicTokenizer()
        self.crftokenizer = CRFPPTokenizer()
        self.hmmtokenizer = HMMTokenizer()

    def parse(self, line, mode='basic'):
        if mode == 'crf':
            tokenizer = self.crftokenizer
        elif mode == 'hmm':
            tokenizer = self.hmmtokenizer
        elif mode == 'basic':
            tokenizer = self.basictokenizer
        return tokenizer.parse(line)


def main(filename, mode='basic'):
    import time
    f = Tokenizer()
    result = []
    ti = time.time()
    with open(filename, "r") as inf:
        for line in inf:
            result.append(f.parse(line.strip(), mode))
    print(time.time() - ti)
    print('\n'.join(result))


if __name__ == "__main__":
    main(os.path.join("data", "test.txt"), "basic")
