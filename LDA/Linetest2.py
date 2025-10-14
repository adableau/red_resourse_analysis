# -*- coding: utf-8 -*-
# 目标： 爬取我国1990---2017年的GDP信息，并绘制图像

import matplotlib.pyplot as plt  # 导入绘图模块 并重命名为plt
import requests  # 导入网页内容抓取包
from bs4 import BeautifulSoup as bs  # 导入网页解析模块 并重命名为bs
from pylab import *  # 该模块是matplotlib的一个子模块
import pandas as pd

rcParams['font.sans-serif'] = ['SimHei']  # 使matplotlib支持中文

year = []  # 横坐标列表
gdp = []  # 纵坐标列表

# pandas csv文档读法
data = pd.read_csv('../data/微博清单_上海红色资源_前100页.csv', sep=',', quotechar='"')
# print(data.head())
# 发布时间,微博内容,转发数,评论数,点赞数
data['发布时间'] = pd.to_datetime(data['发布时间'])
data = data.set_index('发布时间')
# print(data.resample('w').sum())
#print(data.resample('m').sum('评论数'))  # 每个月
#print(data.resample('Q').sum('评论数'))  # 季度
countdata = data.resample('AS').count()
print(countdata)  # 年

yeardata = data.resample('AS').sum()
print(yeardata)  # 年
print(yeardata.点赞数)  # 年
print(yeardata.转发数)  # 年
print(yeardata.评论数)  # 年



