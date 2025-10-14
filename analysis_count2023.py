# -*- coding: utf-8 -*-
#假设csv文件表头页码,微博id,微博作者,发布时间,微博内容,转发数,评论数,点赞数,发布于,ip属地_城市,ip属地_省份,ip属地_国家,主题  统计一下发布时间为2023年、微博内容数量最多的主题是什么
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
plt.rcParams['font.sans-serif'] = ['SimHei']  #设置中文字体
plt.rcParams['axes.unicode_minus'] = False
# 加载CSV文件
# 假设CSV文件路径已正确设置
#file_path = "lycombined_weibo_data.cs"
file_path = "2024031combined_weibo_data.csv"
df = pd.read_csv(file_path)



# 确保 '发布时间' 列是 datetime 类型

# Filter the DataFrame for records with "发布时间" in 2023
df["发布时间"] = pd.to_datetime(df["发布时间"])
df_2023 = df[df["发布时间"].dt.year == 2021]

# Find the most common "主题" in the filtered DataFrame
most_common_topic = df_2023["景"].mode()[0]

print(most_common_topic)




# 将发布时间转换为日期时间格式
df['发布时间'] = pd.to_datetime(df['发布时间'], errors='coerce')

# 过滤发布时间为2023年的数据
df_2023 = df[df['发布时间'].dt.year == 2023]

# 按主题统计微博内容数量
theme_counts = df_2023['景'].value_counts()

# 找出微博内容数量最多的主题及其数量
most_common_theme = theme_counts.idxmax()
most_common_theme_count = theme_counts.max()

# 输出结果
most_common_theme, most_common_theme_count

