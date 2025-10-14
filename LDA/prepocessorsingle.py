# -*- encoding:utf-8 -*-
"""
@author:   Qingchun Bai
"""

import json
import os
import jieba

import csv

import pandas as pd

#
#
#  弹幕转换---按照时间预处理分割
# Add 去重，根据palytime 和 弹幕内容

# #

if __name__ == '__main__':
    # origin_file_dir = '../data/origin_barrage/3/'
    # clean_file_dir = '../data/clean_barrage/3/'
    # extract_barrage(origin_file_dir, clean_file_dir)
    data = pd.read_csv('../data/微博清单_上海红色旅游_前60页.csv', sep=',', quotechar='"')
    # print(data.head())
    # 发布时间,微博内容,转发数,评论数,点赞数
    datacontent = data['微博内容']

    clean_comment_dir = '上海红色旅游text.txt'

    with open(clean_comment_dir, 'w', encoding='utf-8') as f:
        for item in datacontent:
            f.write(item + '\n')  # 将列表的每个元素写到csv文件的一行
