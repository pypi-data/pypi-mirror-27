#! /usr/bin/python
# -*- coding:utf-8 -*-

import os
from . import data_utils


class Tokenizer(object):

    def __init__(self):
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.mode = None

    def parse(self, line):
        sentences = [sentence for sentence in data_utils.segment_split(line)]
        result = map(self._parse, sentences)
        return ' '.join(result)

    def _make_result(self, line, tags):
        result = []
        for n, m in enumerate(tags):
            result.append(line[n])
            if m in ["E", "S"]:
                    result.append(" ")
        result = "".join(result)
        return result
