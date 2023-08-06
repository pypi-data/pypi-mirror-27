#!rusr/bin/python
# -*- coding:utf-8 -*-

import os

from six.moves import cPickle as pickle

from .ops import Tokenizer


class HMMTokenizer(Tokenizer):
    def __init__(self):
        super(HMMTokenizer, self).__init__()
        model_path = os.path.join(self.base_dir, "models", "hmm.m")
        self.model = pickle.load(open(model_path, "rb"))

    def _parse(self, obs):
        """Viterbi

        :param obs: observation or text for tokenize
        :return:
        """
        states, start_p, trans_p, emit_p = self.model

        # fill empty state
        for label in states:
            start_p[label] = start_p.get(label, -3.14e+100)

        for _, sub_node in trans_p.items():
            for label in states:
                sub_node[label] = sub_node.get(label, -3.14e+100)

        # fill new word with -3.14e+100
        for _, sub_node in emit_p.items():
            for label in obs:
                sub_node[label] = sub_node.get(label, -3.14e+100)

        # 路径概率表 V[时间][隐状态] = 概率
        V = [{}]
        # 一个中间变量，代表当前状态是哪个隐状态
        path = {}

        # 初始化初始状态 (t == 0)
        for y in states:
            V[0][y] = start_p[y] + emit_p[y][obs[0]]
            path[y] = [y]

        # 对 t > 0 跑一遍维特比算法
        for t in range(1, len(obs)):
            V.append({})
            newpath = {}
            for y in states:
                # 概率 隐状态 = 前状态是y0的概率 * y0转移到y的概率
                # * y表现为当前状态的概率
                (prob, state) = max([(V[t - 1][y0] +
                                      trans_p[y0][y] +
                                      emit_p[y][obs[t]], y0) for y0 in states])
                # 记录最大概率
                V[t][y] = prob
                # 记录路径
                newpath[y] = path[state] + [y]
            # 不需要保留旧路径
            path = newpath

        (prob, state) = max([(V[len(obs) - 1][y], y) for y in states])
        return self._make_result(obs, path[state])


def main(filename):
    import time
    with open(filename, "r") as inf:
        text = inf.read()

    f = HMMTokenizer()
    ti = time.time()
    result = f.parse(text)
    print(time.time() - ti)
    print(result)


if __name__ == "__main__":
    main(os.path.join("data", "test.txt"))
