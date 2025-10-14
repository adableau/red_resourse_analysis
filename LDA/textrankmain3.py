# -*- encoding:utf-8 -*-
from __future__ import print_function

import codecs
from textrank4zh import TextRank4Keyword, TextRank4Sentence
import pandas as pd

datafile = '../data/微博清单_鲁迅故居_前80页.csv'
data = pd.read_csv(datafile, sep=',', quotechar='"')
# print(data.head())
# 发布时间,微博内容,转发数,评论数,点赞数
datacontent = data['微博内容']
#print(str(datacontent))
# text = codecs.open('alltext.txt', 'r', 'utf-8').read()
tr4w = TextRank4Keyword()

tr4w.analyze(text=str(datacontent), lower=True, window=2)  # py2中text必须是utf8编码的str或者unicode对象，py3中必须是utf8编码的bytes或者str对象

print('关键词：')
for item in tr4w.get_keywords(10, word_min_len=2):
    print(item.word, item.weight)

print()
print('关键短语：')
for phrase in tr4w.get_keyphrases(keywords_num=10, min_occur_num=1):
    print(phrase)

tr4s = TextRank4Sentence()
tr4s.analyze(text=str(datacontent), lower=True, source='all_filters')

print()
print('摘要：')
#for item in tr4s.get_key_sentences(num=20):
#    print(item.index, item.weight, item.sentence)  # index是语句在文本中位置，weight是权重
