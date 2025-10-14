# -*- coding: utf-8 -*-
# 目标： 爬取我国1990---2017年的GDP信息，并绘制图像

import matplotlib.pyplot as plt  # 导入绘图模块 并重命名为plt
import requests  # 导入网页内容抓取包
from bs4 import BeautifulSoup as bs  # 导入网页解析模块 并重命名为bs
from pylab import *  # 该模块是matplotlib的一个子模块
import pandas as pd
import csv
import os

rcParams['font.sans-serif'] = ['SimHei']  # 使matplotlib支持中文


def process_text(filename, clean_comment_dir):
    pathDir = os.listdir(filename)
    namel = []
    datal = []
    for idx, file_name_txt in enumerate(pathDir):
        origin_path = os.path.join(filename, file_name_txt)
        data = pd.read_csv(origin_path, sep=',', quotechar='"')
        print(len(data))
        namel.append(file_name_txt.split('_')[1])
        datal.append(len(data))

    output_csv = "output.csv"  # Replace with your desired output file name
    df = pd.DataFrame({'File_Name': namel, 'Data_Length': datal})
    df.to_csv(output_csv, index=False)


if __name__ == '__main__':
    # origin_file_dir = '../data/origin_barrage/3/'
    # clean_file_dir = '../data/clean_barrage/3/'
    # extract_barrage(origin_file_dir, clean_file_dir)

    origin_comment_dir = '../data/'
    clean_comment_dir = '../LDA/'
    process_text(origin_comment_dir, clean_comment_dir)
