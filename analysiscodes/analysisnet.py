#encoding=gbk
import pandas as pd
import networkx as nx
import itertools
from collections import defaultdict



# 读取数据
df = pd.read_csv('download_weibo_data.csv')

# 使用 jieba 进行中文分词

from collections import Counter
import jieba
#jieba.load_userdict('hit_stopwords.txt')

# 创建停用词list
def stopwordslist(filepath):
    stopwords = [line.strip() for line in open(filepath, 'r',encoding='utf-8').readlines()]
    return stopwords

# 对句子进行分词
def jieba_tokenize(sentence):
    sentence_seged = jieba.cut(sentence.strip())
    stopwords = stopwordslist('hit_stopwords.txt')  # 这里加载停用词的路径
    outstr = ''
    for word in sentence_seged:
        if word not in stopwords:
            if word != '\t':
                outstr += word
                outstr += " "
    return outstr



# 构建共现网络
co_occurrence_graph = nx.Graph()

# 计数器，用于统计每对关键词共现的次数
co_occurrence_counts = defaultdict(int)
words=''
for content in df['微博内容']:
    words = words+jieba_tokenize(content)
    # 使用 itertools.combinations 获取所有可能的词对
for word_pair in itertools.combinations(set(words), 2):
        if word_pair not in co_occurrence_graph:
            co_occurrence_graph.add_edge(*word_pair, weight=0)
        co_occurrence_graph[word_pair[0]][word_pair[1]]['weight'] += 1
        co_occurrence_counts[word_pair] += 1

# 分析网络（例如计算度中心性）
degree_centrality = nx.degree_centrality(co_occurrence_graph)

# 打印度中心性最高的前 10 个节点
top_10 = sorted(degree_centrality.items(), key=lambda x: x[1], reverse=True)[:10]
print("Top 10 nodes by degree centrality:")
for node, centrality in top_10:
    print(f"{node}: {centrality}")

# 可选：绘制网络图（根据需要选择是否执行）
import matplotlib.pyplot as plt
plt.figure(figsize=(12, 12))
pos = nx.spring_layout(co_occurrence_graph, k=0.5)  # k 调整节点之间的距离
nx.draw(co_occurrence_graph, pos, with_labels=True, node_size=50, font_size=10)
plt.show()
