#! /usr/bin/python
# -*- coding:utf-8 -*-

import re
from . import compat

puncs = ['(?=[^0-9A-Z])\.(?=[^0-9a-z])',
         '(?=[^0-9a-z])\.(?=[^0-9A-Z])',
         '。', '．',
         '\?', '？',
         '!', '！',
         ';', '；',
         '…']

delimiter_seg = ['(?=[^0-9A-Z])\.(?=[^0-9a-z])',
                 '(?=[^0-9a-z])\.(?=[^0-9A-Z])',
                 '([0-9]*[a-zA-Z]+[0-9]*)',
                 '。', '．',
                 '\?', '？',
                 '!', '！',
                 ';', '；',
                 '…']

regex = re.compile(compat.as_text('('+'|'.join(puncs)+')'))
delimiter_regex = re.compile(compat.as_text('('+'|'.join(delimiter_seg)+')'))


def segment_split(line):
    line = compat.as_text(line)
    line = line.strip()
    line = delimiter_regex.sub(r"\n\1\n", line)

    segments = []
    for segment in line.split("\n"):
        if len(segment) == 0: continue
        segments.append(segment.strip())
    return segments 

def sentence_split(line):

    line = compat.as_text(line)
    line = line.strip()
    line = regex.sub(r"\1\n", line)

    sentences = []
    for sentence in line.split("\n"):
        if len(sentence) == 0: continue
        sentences.append(sentence.strip())
    return sentences


def tagger(filename):
    """
    将分词文件标注BEMS,并保存，格式如下，每段文字之间用空格隔开
        连  S
        一  S
        捆  S
        麦  S
        也  S
        铡  S
        不  S
        动  S
        呀  S
        ？  S

        他  S
        “ S
        严  B
        格  M
        要  M
    """
    inf = open(filename, "r")
    lines = []
    for line in inf:
        for sentence in sentence_split(line):
            tags = []
            words = re.split("\s+", sentence)
            for word in words:
                if len(word) == 1:
                    tags.append([word[0], "S"])
                elif len(word) == 2:
                    tags.append([word[0], "B"])
                    tags.append([word[-1], "E"])
                elif len(word) >= 3:
                    tags.append([word[0], "B"])
                    for ch in word[1:-1]:
                        tags.append([ch, "M"])
                    tags.append([word[-1], "E"])
            lines.append(tags)

    with open("texts.utf8", "w") as outf:
        for line in lines:
            for word, tag in line:
                outf.write("%s\t%s\n"%(word, tag))
            outf.write("\n")


if __name__ == "__main__":
    #tagger("chinese-text-tokenized.utf8")
    print(sentence_split('2017年12月8日，2017海天盛筵-第八届中国游艇、航空及时尚生活方式展在三亚正式开幕。 本文图片均来自视觉中国'))
