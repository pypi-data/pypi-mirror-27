#! /usr/bin/python
# -*- coding:utf-8 -*-

import os
import CRFPP

from . import compat
from .ops import Tokenizer
from sys import version_info


class CRFPPTokenizer(Tokenizer):

    def __init__(self):
        super(CRFPPTokenizer, self).__init__()
        model_path = os.path.join(self.base_dir, "models", "crf.m")
        self.tagger = CRFPP.Tagger("-m %s -v 3 -n2"%model_path)

    def _parse(self, line):
        line = line.strip()
        self.tagger.clear()
        for token in line:
            if version_info >= (3, 6, 0):
                self.tagger.add(token)
            else:
                self.tagger.add(compat.as_bytes(token))
        self.tagger.parse()
        return self._make_result(line, [self.tagger.y2(idx)
                for idx in range(self.tagger.size())])


def main(filename):
    import time
    with open(filename, "r") as inf:
        text = inf.read()

    f = CRFPPTokenizer()
    ti = time.time()
    result = f.parse(text)
    print(time.time() - ti)
    print(result)


if __name__ == "__main__":
    main(os.path.join("data", "test.txt"))

