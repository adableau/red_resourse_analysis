# -*- encoding:utf-8 -*-
"""
@author:   Qingchun Bai
"""

import json
import os
import jieba

import csv


#
#
#  弹幕转换---按照时间预处理分割
# Add 去重，根据palytime 和 弹幕内容

# #

def dump_to_json(datas, fout):
    for data in datas:
        fout.write(json.dumps(data, sort_keys=True, separators=(',', ': '), ensure_ascii=False))
        fout.write('\n')
    fout.close()


def process(s):
    return list(jieba.cut(s.replace(' ', '')))


def load_from_json(fin):
    datas = []
    for line in fin:
        data = json.loads(line)
        datas.append(data)
    return datas


def read_summary(danmu_path):
    pathDir = os.listdir(danmu_path)
    dict = {}
    for file_name in pathDir:
        data = file_name.split("_")
        dict.setdefault(data[0], data[1])
    return dict


def process_text(filename, out_file):
    pathDir = os.listdir(filename)
    l = []
    i = 0
    for idx, file_name_txt in enumerate(pathDir):
        # clean_path = os.path.join(out_file, file_name_txt)
        # print(file_name_txt)
        origin_path = os.path.join(filename, file_name_txt)
        # file_text_name = file_name_txt.split("_")[1]

        with open(origin_path, 'r', encoding='utf-8', errors='ignore') as fr:
            cr = csv.reader(fr)
            for line in cr:
                l.append(line)
    out_path = os.path.join('alltext.csv')

    with open('alltext.txt', 'w', encoding='utf-8') as f:
        for item in l:
            if item[0] != '﻿页码':
                f.write(item[4]+'\n')  # 将列表的每个元素写到csv文件的一行

    with open(out_path, 'w', encoding='utf-8', newline='') as f2:
        cw = csv.writer(f2)
        # 采用writerow()方法
        for item in l:
            if item[0] != '﻿页码':
                cw.writerow(item[4])  # 将列表的每个元素写到csv文件的一行


def extract_comment(origin_comment_dir, clean_comment_dir):
    pathDir = os.listdir(origin_comment_dir)
    for idx, path in enumerate(pathDir):
        print(idx)
        origin_path = os.path.join(origin_comment_dir, path)
        clean_path = os.path.join(clean_comment_dir, 'clean_' + path)

        comment_list = []
        with open(origin_path, 'r') as fr, open(clean_path, 'w') as fw:
            for i, line in enumerate(fr):
                content_list = line.split('\t')
                # if len(content_list) > 10 and len(content_list[9]) > 5:
                comment_list.append(content_list[6])

            fw.write('\n'.join(comment_list))


if __name__ == '__main__':
    # origin_file_dir = '../data/origin_barrage/3/'
    # clean_file_dir = '../data/clean_barrage/3/'
    # extract_barrage(origin_file_dir, clean_file_dir)

    origin_comment_dir = '../data/'
    clean_comment_dir = '../LDA/'
    process_text(origin_comment_dir, clean_comment_dir)
