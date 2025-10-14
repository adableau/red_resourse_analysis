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


def read_summary(danmu_path):
    pathDir = os.listdir(danmu_path)
    dict = {}
    for file_name in pathDir:
        data = file_name.split("_")
        dict.setdefault(data[0], data[1])
    return dict


def process_danmus(danmu_filename, out_file, summary_dir, dicts=None):
    summary_dicts = read_summary(summary_dir)
    pathDir = os.listdir(danmu_filename)
    for idx, file_name_txt in enumerate(pathDir):
        clean_path = os.path.join(out_file, file_name_txt)
        # print(file_name_txt)
        origin_path = os.path.join(danmu_filename, file_name_txt)
        datas = []
        danmakus = []
        file_id = file_name_txt.split("_")[0]
        if file_id in summary_dicts:  # 可以和video summary 对应上则保存
            with open(origin_path, 'r', encoding='utf8') as fr:
                i = 0
                for line in fr:
                    content_list = line.split('\t')
                    # 分割时序数据，命名文件类型 json

                    if len(content_list) > 10 and len(content_list[9]) > 3:  # 第10列danmaku
                        # print(int((i + 1) / 30), content_list[9])
                        # barage_list.append((i + 1) / 30, content_list[9])
                        oral_comemnt = content_list[9]
                        comment = process(oral_comemnt)  # 分詞加dict
                        if comment not in danmakus:  # 去重
                            datas.append(
                                {'cut': int(i / 30), 'danmaku': oral_comemnt, 'danmaku_clean': " ".join(comment),
                                 'playtime': content_list[6], 'video': content_list[10]})
                            danmakus.append(comment)  # 加入弹幕去重
                            i += 1
            dump_to_json(datas, open(clean_path, 'w', encoding='utf8'))
        else:
            print(file_name_txt)
    print("-----finished---------")


if __name__ == '__main__':
    # origin_file_dir = '../data/origin_barrage/3/'
    # clean_file_dir = '../data/clean_barrage/3/'
    # extract_barrage(origin_file_dir, clean_file_dir)

    origin_comment_dir = 'G:/2019-09-old/0000-danmaku_data/00-Data/Entertainment-danmaku/'
    clean_comment_dir = '../data/new_clean_danmu_20191205/'
    summary_dir = 'E:\danmu-201909\data\Entertainment_summary/'
    process_danmus(origin_comment_dir, clean_comment_dir, summary_dir)
