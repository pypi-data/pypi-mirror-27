#! /usr/bin/python
# -*- coding:utf-8 -*-

from six.moves import cPickle as pickle
import re
import data_utils


def learn(infile):
    regex = re.compile('\s+')
    prob = {"#count":0}
    with open(infile, 'r') as inf:
        for line in inf:
            for l in data_utils.sentence_split(line):
                last_token = "#START#"
                for token in regex.split(l):
                    prob[last_token] = prob.get(last_token, {})
                    prob[last_token][token] = prob[last_token].get(token, 0) + 1
                    prob["#count"] += 1
                    last_token = token
    with open("models/basic.m", "wb") as outf:
        pickle.dump(prob, outf, protocol=2)


def get_from_dict(infile):
    regex = re.compile('\s+')
    model = {'#count':0}
    with open(infile, 'r') as inf:
        for line in inf:
            for l in data_utils.sentence_split(line):
                for token in regex.split(l):
                    model["#count"] += 1
                    node = model
                    for char in token:
                        node[char] = node.get(char, ({}, {}))
                        sub_node, end = node[char]
                        node = sub_node
                    end[token] = end.get(token, 0) + 1

    with open("models/tokens.m", "wb") as outf:
        pickle.dump(model, outf, protocol=2)


def add_dict(modelfile, infile):
    with open(modelfile, 'rb') as inf:
        model = pickle.load(inf)

    with open(infile, 'r') as inf:
        for token in inf:
            token = token.strip()
            model["#count"] += 1
            node = model
            for char in token:
                node[char] = node.get(char, ({}, {}))
                sub_node, end = node[char]
                node = sub_node
            end[token] = end.get(token, 0) + 1

    with open("tokens.m", "wb") as outf:
        pickle.dump(model, outf, protocol=2)


if __name__ == "__main__":
    # infile = 'corpus/chinese-text-tokenized.utf8'
    # learn(infile)
    # get_from_dict(infile)
    add_dict('models/tokens.m', 'corpus/dictionary/chinesewords.dict')

