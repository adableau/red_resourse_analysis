# -*- encoding:utf-8 -*-
"""
@author:   Qingchun Bai
"""

import json
import os
import jieba


#
#
#  剧情简介分割处理
# #

def dump_to_json(datas, fout):
    for data in datas:
        fout.write(json.dumps(data, sort_keys=True, separators=(',', ': '), ensure_ascii=False))
        fout.write('\n')
    fout.close()


def dict_from_json(fin):
    dict = {}
    for line in fin:
        data = json.loads(line)
        dict.setdefault(data.get("tv_name"), data.get("tv_Id"))
    return dict


def process_summary(danmu_path, out_file, tv_info):
    pathDir = os.listdir(danmu_path)
    tv_info_datas = dict_from_json(open(tv_info, 'r', encoding='utf8'))

    for idx, file_name in enumerate(pathDir):
        # print(file_name)  # 313099899_特警力量 DVD版.txt
        file_name_s = file_name.split("_")[2].split(".")[0]  # 特警力量 DVD版

        origin_path = os.path.join(danmu_path, file_name)

        with open(origin_path, 'r', encoding='utf8') as fr:
            for i, line in enumerate(fr):  # 每一集N句摘要
                datas = []
                content_list = line.split('###')
                tv_name = file_name_s + str(i + 1)
                video_id = tv_info_datas.get(tv_name)
                if video_id is not None:
                    title = tv_name
                    contents = content_list[2].split('。')[:-1]
                    if len(contents) > 0:
                        for j, data in enumerate(contents):
                            datas.append({'video': video_id, 'cut': j + 1, 'content': data, 'title': title,
                                          'lengths': len(contents)})
                        clean_path = os.path.join(out_file, str(video_id) + "_" + title + "_" + str(len(contents)))
                        # print(clean_path)
                        dump_to_json(datas, open(clean_path, 'w', encoding='utf8'))  # 每一集存一个文件
                else:
                    # 找不到对应id
                    print(tv_name)


if __name__ == '__main__':
    # origin_file_dir = '../data/origin_barrage/3/'
    # clean_file_dir = '../data/clean_barrage/3/'
    # extract_barrage(origin_file_dir, clean_file_dir)

    # TVinfo 和summary 对应
    # danmu_path = 'G:\0000-danmaku_data\00-Data\Entertainment_summary'
    # out_file = 'G:\0000-danmaku_data\00-Data\NewEntertainment_summary'
    # danmu_path = '../data/Entertainment_summary'
    # out_file = '../data/out_Entertainment_summary'
    # tv_info = '../data/tv_information.json'
    danmu_path = 'G:/2019-09-old/0000-danmaku_data/00-Data/Entertainment_summary/'
    # clean_comment_dir = '../data/clean_comment_cut/'
    out_file = '../data/Entertainment_summary/'
    tv_info = 'E:\danmu-201909\data/tv_information.json'

    process_summary(danmu_path, out_file, tv_info)
