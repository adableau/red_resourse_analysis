# -*- encoding:utf-8 -*-
"""
@author:   Qingchun Bai
"""

import json
import os
import jieba
import csv
import random
import codecs
import file_utils


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
    try:
        if os.path.exists(file_path):
            lines = open(file_path, 'r', encoding='utf8').read().strip().split('\n')
            for line in lines:
                data = json.loads(line)
                datas.append(data)
            return datas
    except Exception:
        return None


# process_danmus(origin_comment_dir, data_sava_path, summary_dir)
def process_danmus(summary_dir, data_sava_path, origin_comment_dir, dicts=None):
    pathDir = os.listdir(summary_dir)
    info = []

    for idx, file_name_txt in enumerate(pathDir):
        danmus = ""
        danmu_file = file_name_txt.split("_")
        danmu_file_path = os.path.join(origin_comment_dir, danmu_file[0])
        origin_path = os.path.join(clean_summary_dir, file_name_txt)

        summary = file_utils.load_danmu(origin_path)
        danmu = file_utils.load_danmu(danmu_file_path)
        video_time_slice = []
        for i, n in enumerate(summary):
            video_time_slice.append(n["video"].split("-")[1])

        ps_init = 0
        cut_num_init = 0
        # n个剧情简介对应M块弹幕
        similarity_list = []
        danmu_cut_len = len(danmu)
        summary_cut_len = len(summary)
        # 均分,每一份长度
        cut_num = int(danmu_cut_len / summary_cut_len)


        for i,m in enumerate(danmu):

            if i<= cut_num*(cut_num_init+1):
                danmus += m["danmaku_clean"]
            else:
                info.append(danmus)
                cut_num_init += 1
                danmus=""


        with open(data_sava_path, "w", encoding="UTF-8", newline="") as csvfile:  ##“ ab+ ”去除空白行，又叫换行！
            # csvfile.write(codecs.BOM_UTF8)  ##存入表内的文字格式
            writer = csv.writer(csvfile)  # 存入表时所使用的格式
            writer.writerow(['danmu'])
            writer.writerows(info)  # 写入表
            print("-finish---")


if __name__ == '__main__':
    # origin_file_dir = '../data/origin_barrage/3/'
    # clean_file_dir = '../data/clean_barrage/3/'
    # extract_barrage(origin_file_dir, clean_file_dir)
    # stopword_dir = '../data/stopword/stopWords.txt'

    clean_comment_cut_dir = '../data/pairs/danmaku'
    clean_summary_dir = '../data/pairs/summary'
    matrix_similarity_dir = '../data/embeding_matrix_similarity/'
    # method = "jaccard_similarity"
    data_sava_path = "../data/ldadanmu.csv"

    # get_similarity(method, clean_summary_dir, clean_comment_cut_dir, matrix_similarity_dir)

    process_danmus(clean_summary_dir, data_sava_path, clean_comment_cut_dir, matrix_similarity_dir)

    # process_danmus(origin_comment_dir, data_sava_path, summary_dir)
    print("---finished---")
