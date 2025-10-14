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
def process_danmus(origin_comment_dir, data_sava_path, summary_dir, dicts=None):
    pathDir = os.listdir(origin_comment_dir)

    summary_path_dir = os.listdir(summary_dir)

    info = []

    for idx, file_name_txt in enumerate(summary_path_dir):
        n1, n2, n3 = file_name_txt.split("_", 2)
        origin_summary_path = os.path.join(summary_dir, file_name_txt)
        origin_danmu_path = os.path.join(origin_comment_dir, n1 + "_" + n2 + ".txt")
        try:
            danmu_all_list = load_danmu(origin_danmu_path)
            summary_all_list = load_danmu(origin_summary_path)
            if danmu_all_list is None:
                continue
            s_len = len(summary_all_list) - 1
            d_len = len(danmu_all_list) - 1

            print(d_len)
        except Exception:
            continue

        if d_len < 20:
            continue

        for i in range(20):
            # 头部
            dt = []
            dt.append(summary_all_list[0].get("content"))
            dt.append(danmu_all_list[i].get("danmaku"))
            dt.append("1")
            info.append(dt)
            # 尾部
            dt = []
            dt.append(summary_all_list[s_len].get("content"))
            dt.append(danmu_all_list[d_len - i].get("danmaku"))
            dt.append("1")
            info.append(dt)

            # 负样本
            slice_list = random.sample(danmu_all_list, 6)
            # 随机采样正负样
            for slice in slice_list:

                if (int(slice["cut"]) == 2 or int(slice["cut"])  == 3):
                    dt = []
                    dt.append(summary_all_list[0].get("content"))
                    dt.append(slice["danmaku"])
                    dt.append("1")
                elif (int(slice["cut"]) >= 30):
                    dt = []
                    dt.append(summary_all_list[0].get("content"))
                    dt.append(slice["danmaku"])
                    dt.append("0")

            info.append(dt)


    with open(data_sava_path, "w", encoding="UTF-8", newline="") as csvfile:  ##“ ab+ ”去除空白行，又叫换行！
        # csvfile.write(codecs.BOM_UTF8)  ##存入表内的文字格式
        writer = csv.writer(csvfile)  # 存入表时所使用的格式
        writer.writerow(['summary', 'danmu', 'label'])
        writer.writerows(info)  # 写入表


if __name__ == '__main__':
    # origin_file_dir = '../data/origin_barrage/3/'
    # clean_file_dir = '../data/clean_barrage/3/'
    # extract_barrage(origin_file_dir, clean_file_dir)
    # stopword_dir = '../data/stopword/stopWords.txt'
    origin_comment_dir = 'E:\danmu-201909\data/new_clean_danmu_20191205/'
    clean_comment_dir = '../data/new_clean_danmu_cut/'
    summary_dir = 'E:\danmu-201909\data\Entertainment_summary/'
    data_sava_path = "../data/new_danmudata_P_N.csv"
    process_danmus(origin_comment_dir, data_sava_path, summary_dir)
    print("---finished---")
