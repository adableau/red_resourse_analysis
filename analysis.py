import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx  # 用于语义网络分析
from collections import Counter

# 读取 CSV 文件
df = pd.read_csv('your_data.csv')

# 1. 统计关注数量（这里假设是统计每个微博作者的微博数量）
author_counts = df['微博作者'].value_counts()

# 2. 关注度年际变化（基于微博的发布年份）
df['发布时间'] = pd.to_datetime(df['发布时间'])
df['年份'] = df['发布时间'].dt.year
yearly_counts = df.groupby('年份').size()

# 绘制年际变化图
yearly_counts.plot(kind='bar')
plt.title('Yearly Weibo Counts')
plt.xlabel('Year')
plt.ylabel('Number of Weibos')
plt.show()

# 3. 语义网络分析（这里提供一个基本思路，但实现起来相对复杂）
# 示例：从微博内容中提取关键词并构建网络
# 这需要进一步的文本处理和专业知识

# 假设函数 extract_keywords 用于从文本中提取关键词
def extract_keywords(text):
    # 这里应该是一个复杂的文本处理过程，可能涉及到自然语言处理技术
    # 例如使用 jieba, NLTK 或其他库来提取关键词
    return []

# 构建网络
G = nx.Graph()
for content in df['微博内容']:
    keywords = extract_keywords(content)
    for keyword in keywords:
        for other in keywords:
            if keyword != other:
                G.add_edge(keyword, other)

# 绘制网络
nx.draw(G, with_labels=True)
plt.show()
