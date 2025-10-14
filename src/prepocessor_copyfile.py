# -*- encoding:utf-8 -*-
"""
@author:   Qingchun Bai
"""

import json
import os
import jieba

#导入shutil模块和os模块
import shutil,os

#
#
#  弹幕转换---将弹幕按照时间预处理分割为弹幕片段
# #

def process_danmus(filename, out_file,):
    #summary_dicts = read_summary(summary_dir)
    pathDir = os.listdir(filename)
    for idx, file_name_txt in enumerate(pathDir):
        # print(file_name_txt)
        origin_path = os.path.join(filename, file_name_txt)
        file_id = file_name_txt.split("_")[0]
        new_path = os.path.join(out_file, file_id)

        # 复制并重命名新文件
        shutil.copy(origin_path, new_path)




if __name__ == '__main__':
    # origin_file_dir = '../data/origin_barrage/3/'
    # clean_file_dir = '../data/clean_barrage/3/'
    # extract_barrage(origin_file_dir, clean_file_dir)

    origin_comment_dir = 'G:/2019-09-old/0000-danmaku_data/00-Data/Entertainment-danmaku/'
    clean_comment_dir = 'E:\danmu-201909/data/clean_comment_cut/'
    new_comment_dir = 'E:\danmu-201909/data/clean_comment_cut_new/'
    process_danmus( clean_comment_dir, new_comment_dir)
