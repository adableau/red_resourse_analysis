import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx  # 用于语义网络分析
from collections import Counter

plt.rcParams['font.sans-serif'] = ['SimHei']  #设置中文字体
plt.rcParams['axes.unicode_minus'] = False
import matplotlib.pyplot as plt

# 总数量和负向数量
total_count = 19048
negative_count = 1431
positive_count = total_count - negative_count
print(positive_count)
# 数据和标签
counts = [positive_count, negative_count]
labels = ['正向', '负向']

# 创建柱状图
plt.figure(figsize=(8, 6))
plt.bar(labels, counts, color=['red', 'blue'])

# 添加标题和标签
plt.title('情感数量分布')
plt.xlabel('微博情感')
plt.ylabel('数量')

# 显示图形
plt.show()

