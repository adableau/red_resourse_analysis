# -*- encoding:utf-8 -*-
"""
@author:   Qingchun Bai
"""

import json
import os
import jieba
import prepocessor


#
#
#  剧情简介分割处理
# #

def process_summary(danmu_path, out_file, tv_info):
    pathDir = os.listdir(danmu_path)
    tv_info_datas = prepocessor.load_from_json(open(tv_info, 'r', encoding='utf8'))

    for idx, file_name in enumerate(pathDir):
        print(file_name)  # 313099899_summary_特警力量 DVD版.txt
        file_name_s = file_name.split("_")[1].split(".")[0]  # 特警力量 DVD版

        origin_path = os.path.join(danmu_path, file_name)

        with open(origin_path, 'r', encoding='utf8') as fr:
            for i, line in enumerate(fr):  # 每一集N句摘要保存一個文件
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
                        print(clean_path)
                    prepocessor.dump_to_json(datas, open(clean_path, 'w', encoding='utf8'))  # 每一集存一个文件
                else:
                    print(video_id)
                    print(tv_name)


if __name__ == '__main__':
    # TVinfo 和summary 对应
    # danmu_path = 'G:\0000-danmaku_data\00-Data\Entertainment_summary'
    # out_file = 'G:\0000-danmaku_data\00-Data\NewEntertainment_summary'
    #danmu_path = '../data/Entertainment_summary'
    #out_file = '../data/out_Entertainment_summary'
    tv_info = 'E:\danmu-201909\data/tv_information.json'

    origin_comment_dir = 'G:/2019-09-old/0000-danmaku_data/00-Data/Entertainment-danmaku/'
    #clean_comment_dir = '../data/clean_comment_cut/'
    out_file = '../data/Entertainment_summary/'

    process_summary(origin_comment_dir, out_file,tv_info)
