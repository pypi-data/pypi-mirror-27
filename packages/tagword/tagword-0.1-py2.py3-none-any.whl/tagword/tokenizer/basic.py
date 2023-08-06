#! /usr/bin/python
# -*- coding:utf-8 -*-

import os
import re
import math
from six.moves import cPickle as pickle

from .ops import Tokenizer
from ..wordiscovery import WordDiscovery


regex = re.compile("\s+")
regex_alphabet = re.compile("[0-9]*[a-zA-Z]+[0-9]*")


class BasicTokenizer(Tokenizer):

    def __init__(self):
        super(BasicTokenizer, self).__init__()
        model_path = os.path.join(self.base_dir, "models", "basic.m")
        token_path = os.path.join(self.base_dir, "models", "tokens.m")
        self.model = pickle.load(open(model_path, "rb"))
        self.token = pickle.load(open(token_path, "rb"))
        self.mode = 'basic'

    def add(self, custom_dict):

        for token, freq in custom_dict:
            token = token.strip()
            self.token["#count"] += freq
            node = self.token
            for char in token:
                node[char] = node.get(char, ({}, {}))
                sub_node, end = node[char]
                node = sub_node
            end[token] = end.get(token, 0) + freq

    def add_custom(self, custom_dict):
        self.add(custom_dict)

    def _parse(self, 
               line,
               custom_dict=None):
        if custom_dict:
            self.add_custom
            
        line = line.strip()
        # line = regex.sub("", line)
        last_nodes = []
        V = [{"#START#": 0.0}]
        path = {"#START#":["#START#"]}

        alphabet_state = None
        if regex_alphabet.match(line):
            return line
        for idx in range(len(line)):
            char = line[idx]
            new_nodes = []
            tokens = []

            # Step 1, search all possible tokens
            for node in last_nodes + [self.token]:
                next_node, e = node.get(char, ({}, {}))
                new_nodes.append(next_node)
                if e:
                    tokens.append([[k, v] for k, v in e.items()][0])
            last_nodes = new_nodes

            if len(tokens) == 0:
                tokens = [[char, 1]]

            # Step 2, calculate each token with last state which is counted by token length
            V.append({})
            for tokencounter in tokens:
                token, counter = tokencounter
                token_length = len(token)
                start_idx = idx + 1 - token_length
                token_freq = math.log(float(counter) / self.token['#count'])
                in_tk = []
                for last_word, prob in V[start_idx].items():
                    self.model[last_word] = self.model.get(last_word, {})
                    pair_freq = math.log(float(self.model[last_word].get(token, 1)) / self.model['#count'])
                    score = token_freq+pair_freq
                    in_tk.append([prob + score, last_word, token])
                max_in_tk = max(in_tk)
                (prob, state, token) = max_in_tk
                V[idx+1][token] = prob
                path[token] = path[state] + [token]

        (prob, state) = max([(V[-1][y], y) for y in V[-1]])
        return ' '.join(path[state][1:])
