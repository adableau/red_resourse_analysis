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
plt.rcParams['font.sans-serif'] = ['SimHei']  #设置中文字体
plt.rcParams['axes.unicode_minus'] = False
# 加载CSV文件
# 假设CSV文件路径已正确设置
#file_path = "lycombined_weibo_data.cs"
file_path = "shanghai.csv"

import pandas as pd

# 读取CSV文件
df = pd.read_csv(file_path, header=None,error_bad_lines=False)

# 定义函数以处理列数超过13的情况
def merge_columns(row):
    if len(row) > 13:
        # 合并第5列到倒数第8列，并将合并后的数据放回第5列
        # 先将英文逗号替换为中文逗号，然后合并
        merged_content = '，'.join(row[4:-8]).replace(",", "，")
        row[4] = merged_content
        # 删除多余的列，只保留前13列
        row = row[:5].tolist() + row[-8:].tolist()
    return row

# 应用函数到每一行
df = df.apply(merge_columns, axis=1)

# 输出结果到新的CSV文件
df.to_csv('cleaned_shanghai.csv', index=False, header=False)
