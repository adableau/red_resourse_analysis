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
# Add 弹幕去重，根据palytime 和 弹幕内容

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


def process_danmus(filename, out_file, summary_dir, dicts=None):
    # summary_dicts = {}
    pathDir = os.listdir(filename)
    for idx, file_name_txt in enumerate(pathDir):
        clean_path = os.path.join(out_file, file_name_txt)
        # print(file_name_txt)
        origin_path = os.path.join(filename, file_name_txt)
        datas = []
        danmakus = []
        with open(origin_path, 'r', encoding='utf8') as fr:
            for line in fr:
                data = json.loads(line)
                danmaku = data["danmaku"]
                if danmaku not in danmakus:
                    datas.append(data)
                    danmakus.append(danmaku)
        dump_to_json(datas, open(clean_path, 'w', encoding='utf8'))


if __name__ == '__main__':
    # origin_file_dir = '../data/origin_barrage/3/'
    # clean_file_dir = '../data/clean_barrage/3/'
    # extract_barrage(origin_file_dir, clean_file_dir)

    origin_comment_dir = 'E:\danmu-201909\data\clean_comment_cut_new/'
    clean_comment_dir = '../data/new_clean_danmu_cut/'
    summary_dir = '../data/Entertainment_summary/'
    process_danmus(origin_comment_dir, clean_comment_dir, summary_dir)
