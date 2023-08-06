#! /usr/bin/python
# -*- coding:utf-8 -*-

from six.moves import cPickle as pickle
import re
import math


def learn(filename, modelname):
    states = ["B", "M", "E", "S"]
    start_p = {'label': {}, 'count': 0}
    trans_p = {'B': {'label': {}, 'count': 0},
               'M': {'label': {}, 'count': 0},
               'E': {'label': {}, 'count': 0},
               'S': {'label': {}, 'count': 0}}
    emit_p = {'B': {'label': {}, 'count': 0},
              'M': {'label': {}, 'count': 0},
              'E': {'label': {}, 'count': 0},
              'S': {'label': {}, 'count': 0}}
    regex = re.compile("\s+")

    def add_data(node, tag):
        node['label'][tag] = node['label'].get(tag, 0) + 1
        node['count'] = start_p.get('count', 0) + 1

    with open(filename, "r") as inf:
        last_label = None
        for line in inf:
            line = line.strip()
            if len(line) > 0:
                token, label = regex.split(line)
                add_data(emit_p[label], token)
                if last_label is None:
                    add_data(start_p, label)
                else:
                    add_data(trans_p[last_label], label)
                last_label = label
            else:
                last_label = None

    def calc_log(node):
        count = math.log(node['count'])
        sub_node = {}
        for k, v in node['label'].items():
            # sub_node['label'][k] = math.log(v) - count  # keep 'label' key in dict
            sub_node[k] = math.log(v) - count
        return sub_node

    start_p = calc_log(start_p)
    for label in states:
        emit_p[label] = calc_log(emit_p[label])
        trans_p[label] = calc_log(trans_p[label])

    with open(modelname, 'wb') as outf:
        pickle.dump([states, start_p, trans_p, emit_p], outf, protocol=2)


if __name__ == "__main__":
    learn("text_tag.utf8", 'hmm.m')

