# -*- encoding:utf-8 -*-
"""
@author:   Qingchun Bai
"""

import json
import os
import jieba


#
#
#  弹幕转换---将弹幕按照时间预处理分割为弹幕片段
# 　 Add 弹幕去重，根据palytime 和 弹幕内容
# 　去除停用词

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


# 创建停用词list
def stopwordslist(filepath):
    stopwords = [line.strip() for line in open(filepath, 'r').readlines()]
    return stopwords


def load_danmu(file_path):
    datas = []
    lines = open(file_path, 'r', encoding='utf8').read().strip().split('\n')
    for line in lines:
        data = json.loads(line)
        datas.append(data)
    return datas


def process_danmus(filename, out_file, summary_dir, stopword_dir, dicts=None):
    pathDir = os.listdir(filename)
    # todo read stopwords
    stopwords = stopwordslist(stopword_dir)
    summary_path_dir = os.listdir(summary_dir)
    for idx, file_name_txt in enumerate(pathDir):

        summary_path = os.path.join(filename, file_name_txt)


    for idx, file_name_txt in enumerate(pathDir):
        clean_path = os.path.join(out_file, file_name_txt)
        print(file_name_txt)
        origin_path = os.path.join(filename, file_name_txt)
        new_data_list = []
        data_list = load_danmu(origin_path)
        for data in data_list:
            new_danmaku = ""
            for w in data["danmaku"].split(" "):
                if w not in stopwords:
                    new_danmaku += w + " "
            data["danmaku_clean"] = new_danmaku

            new_data_list.append(data)
        dump_to_json(new_data_list, open(clean_path, 'w', encoding='utf8'))


if __name__ == '__main__':
    # origin_file_dir = '../data/origin_barrage/3/'
    # clean_file_dir = '../data/clean_barrage/3/'
    # extract_barrage(origin_file_dir, clean_file_dir)
    stopword_dir = '../data/stopword/stopWords.txt'
    origin_comment_dir = '../data/pairs/danmaku/'
    clean_comment_dir = '../data/new_clean_danmu_cut/'
    summary_dir = '../data/pairs/summary/'
    process_danmus(origin_comment_dir, clean_comment_dir, summary_dir, stopword_dir)
