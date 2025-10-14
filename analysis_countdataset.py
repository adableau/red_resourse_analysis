# -*- coding: utf-8 -*-
import jieba
import pandas as pd
import networkx as nx
import itertools
from collections import defaultdict

# 读取数据

import pandas as pd
from datetime import datetime

# 重新定义之前的函数，以便于重新执行代码状态
from nltk import word_tokenize
from nltk.corpus import stopwords

from data_utils import save_datas
import pandas as pd
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei']  #设置中文字体
plt.rcParams['axes.unicode_minus'] = False
from collections import Counter
# 加载CSV文件
# 假设CSV文件路径已正确设置
#file_path = "lycombined_weibo_data.cs"
file_path = "2024031combined_weibo_data.csv"
df = pd.read_csv(file_path)



# 确保 '发布时间' 列是 datetime 类型
df['发布时间'] = pd.to_datetime(df['发布时间'])

# 提取年份作为新列
df['年份'] = df['发布时间'].dt.year

# 按年份分组并汇总转发数，评论数，点赞数
grouped_data_by_year = df.groupby('年份').agg({
    '微博id': 'count',
    '转发数': 'sum',
    '评论数': 'sum',
    '点赞数': 'sum'
}).reset_index()

# 总微博数（对所有记录计数）
content_count = len(df)

df['微博内容'] = df['微博内容'].astype(str)
# Count the number of unique authors in the '微博作者' column
unique_authors_count = df['微博作者'].nunique()
print('unique_authors_count is')
print(unique_authors_count)
# Calculate average comment length
df['评论长度'] = df['微博内容'].apply(len)
average_length = df['评论长度'].mean()

# Calculate minimum, maximum, and median length of comments
min_length = df['评论长度'].min()
max_length = df['评论长度'].max()
median_length = df['评论长度'].median()
print('len_count is')
print(average_length)


print('min_length is')
print(min_length)

print('max_length is')
print(max_length)

print('median_length is')
print(median_length)



# 数据预处理
# 假设微博内容在列 '微博内容'
texts = df['微博内容'].astype(str)

all_comments = ' '.join(texts)
words = jieba.lcut(all_comments)  # Segment the text into words

stop_words = set(stopwords.words('chinese'))  # 请确保这里使用正确的语言
filtered_words = [[word for word in doc if word not in stop_words and word.isalpha() and len(word) > 1] for doc in texts]
# Calculate the frequency of each word
word_counts = Counter(filtered_words)
top_10_words = word_counts.most_common(10)
print("Top 10 Frequent Words:")
for word, count in top_10_words:
    print(f"{word}: {count}")


# 准备按年份汇总的数据
data_by_year = {
    "年份": grouped_data_by_year['年份'].tolist(),
    "微博数": grouped_data_by_year['微博id'].tolist(),  # 每个年份重复总微博数
    "点赞数": grouped_data_by_year['点赞数'].tolist(),
    "转发数": grouped_data_by_year['转发数'].tolist(),
    "评论数": grouped_data_by_year['评论数'].tolist()
}

# 使用这些数据创建DataFrame，以便进一步操作或可视化
df = pd.DataFrame(data_by_year)

# 如果你需要按'景点'列的点赞数汇总（假设列名正确）
#likes_by_spot = df.groupby('景点')['点赞数'].sum().reset_index()

# 现在，'summary_df_by_year' 包含按年份汇总的数据，
# 'likes_by_spot' 包含按景点汇总的点赞数。



# 绘制图形
# plt.figure()

plt.plot(df["年份"].to_numpy(), df["微博数"].to_numpy(), marker='o', label='微博数')
plt.plot(df["年份"].to_numpy(), df["点赞数"].to_numpy(), marker='o', label='点赞数')
plt.plot(df["年份"].to_numpy(), df["转发数"].to_numpy(), marker='o', label='转发数')
plt.plot(df["年份"].to_numpy(), df["评论数"].to_numpy(), marker='o', label='评论数')

plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False #用来正常显示负号

#plt.title(u"‘上海红色旅游’关键词的微博爬虫数据年际变化")
#plt.title(u"‘上海红色资源’关键词的微博爬虫数据年际变化")
plt.title(u"上海红色旅游微博数据年际变化")
plt.xlabel(u"年份")
plt.ylabel(u"数量/条")
plt.legend()

plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()