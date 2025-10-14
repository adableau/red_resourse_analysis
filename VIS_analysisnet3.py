# -*- coding: utf-8 -*-
import pandas as pd
import networkx as nx
import itertools
from collections import defaultdict

# 读取数据
import pandas as pd
from datetime import datetime

# 重新定义之前的函数，以便于重新执行代码状态
from data_utils import save_datas
import pandas as pd
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei']  # 设置中文字体
plt.rcParams['axes.unicode_minus'] = False
# 加载CSV文件
# 假设CSV文件路径已正确设置
#file_path = "combined_weibo_data.csv"
file_path = "2024031combined_weibo_data.csv"
df = pd.read_csv(file_path)

#202410最新

# Data for the chart
locations = [
    '中共一大会址', '上海鲁迅纪念馆', '海关大楼', '鲁迅墓', '新新公司', '龙华革命烈士纪念地',
    '陈云纪念馆', '无名烈士墓', '先施公司', '中共四大纪念馆', '留法勤工俭学出发地',
    '上海宋庆龄故居', '中共二大会址', '上海中山故居', '上海茂名路毛泽东旧居',
    '上海邮政总局', '上海孙中山故居纪念馆', '中共中央政治局机关旧址', '韬奋纪念馆', '储能中学'
]
weibo_counts = [
    1310, 681, 591, 487, 472, 434, 429, 403, 373, 371, 353, 385, 333, 296, 295,
    287, 284, 301, 268, 262
]

# Create the bar chart
plt.figure(figsize=(10, 8))
plt.barh(locations, weibo_counts, color='red')
plt.xlabel(u'微博数量/条')
plt.ylabel(u'红色资源点位名称')
plt.title(u'“微博”上海红色资源数量前20点位')
plt.gca().invert_yaxis()  # 反转Y轴，使得顶部的条形是最高值
plt.tight_layout()  # 自动调整布局，防止标签被截掉
plt.show()


# 按景点名称统计评论数
# 按照景点名称聚合数据，并计算每个景点的总评论数
comment_counts = df.groupby('景').count().reset_index()
# 过滤掉'景'列中值为"A"或"B"的行
comment_counts = comment_counts[~comment_counts['景'].isin(['鲁迅故居', '上海红色资源', '上海 红色寻访', '上海红色旅游', '李白烈士'])]

# 按照评论数降序排序，并选取前20个
top_20_spots = comment_counts.sort_values(by='微博内容', ascending=False).head(20)
print(top_20_spots['景'])
# 生成柱状图
plt.figure(figsize=(10, 8))  # 设置图形的大小
plt.barh(top_20_spots['景'], top_20_spots['微博内容'], color='red')  # 创建水平柱状图
plt.xlabel(u"总微博数")  # X轴标签
plt.ylabel(u"景点名称")  # Y轴标签
plt.title(u"按景点名称统计的微博数排行前20")  # 图形标题
plt.gca().invert_yaxis()  # 反转Y轴，使得顶部的条形是最高值
plt.tight_layout()  # 自动调整布局，防止标签被截掉
plt.show()

# 按景点名称统计评论数
# 按照景点名称聚合数据，并计算每个景点的总评论数
comment_counts = df.groupby('景')['评论数'].sum().reset_index()
# 过滤掉'景'列中值为"A"或"B"的行
comment_counts = comment_counts[~comment_counts['景'].isin(['鲁迅故居', '上海红色资源', '上海 红色寻访', '上海红色旅游', '李白烈士'])]

# 按照评论数降序排序，并选取前20个
top_20_spots = comment_counts.sort_values(by='评论数', ascending=False).head(30)

# 生成柱状图
plt.figure(figsize=(10, 8))  # 设置图形的大小
plt.barh(top_20_spots['景'], top_20_spots['评论数'], color='green')  # 创建水平柱状图
plt.xlabel(u"总评论数")  # X轴标签
plt.ylabel(u"景点名称")  # Y轴标签
plt.title(u"按景点名称统计的网络评论数排行前20")  # 图形标题
plt.gca().invert_yaxis()  # 反转Y轴，使得顶部的条形是最高值
plt.tight_layout()  # 自动调整布局，防止标签被截掉
plt.show()


# 按景点名称统计dianzan数
# 按照景点名称聚合数据，并计算每个景点的总评论数
comment_counts_dz = df.groupby('景')['点赞数'].sum().reset_index()

# 过滤掉'景'列中值为"A"或"B"的行
comment_counts = comment_counts[~comment_counts['景'].isin(['鲁迅故居', '上海红色资源', '上海红色旅游', '李白烈士'])]

# 按照评论数降序排序，并选取前20个
top_20_spots = comment_counts_dz.sort_values(by='点赞数', ascending=False).head(20)

# 生成柱状图
plt.figure(figsize=(10, 8))  # 设置图形的大小
plt.barh(top_20_spots['景'], top_20_spots['点赞数'], color='blue')  # 创建水平柱状图
plt.xlabel(u"总点赞数")  # X轴标签
plt.ylabel(u"景点名称")  # Y轴标签
plt.title(u"按景点名称统计的网络点赞排行前20")  # 图形标题
plt.gca().invert_yaxis()  # 反转Y轴，使得顶部的条形是最高值
plt.tight_layout()  # 自动调整布局，防止标签被截掉
plt.show()
