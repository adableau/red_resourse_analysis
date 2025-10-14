# -*- coding: utf-8 -*-
import pandas as pd
import networkx as nx
import itertools
from collections import defaultdict

# 读取数据

import pandas as pd
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt

# 创建数据
data = {
    '年份': [2022, 2023, 2024],
    '微博数': [157, 613, 1400],
    '点赞数': [9784, 34677, 33359],
    '转发数': [3581, 7886, 6010],
    '评论数': [1375, 4297, 6364]
}

# 转换为 DataFrame
df = pd.DataFrame(data)

# 设置图形大小
plt.figure(figsize=(10, 6))

# 绘制折线图
plt.plot(df['年份'], df['微博数'], marker='o', label='微博数')
plt.plot(df['年份'], df['点赞数'], marker='o', label='点赞数')
plt.plot(df['年份'], df['转发数'], marker='o', label='转发数')
plt.plot(df['年份'], df['评论数'], marker='o', label='评论数')

# 添加标题和标签
plt.title('年份与社交媒体指标的关系')
plt.xlabel('年份')
plt.ylabel('数量')
plt.legend()

# 显示图形
plt.grid(True)
plt.show()
