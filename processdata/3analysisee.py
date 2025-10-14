import pandas as pd
import jieba
import jieba.analyse
from collections import Counter
import re

# 加载数据
#data = pd.read_csv('人民英雄纪念碑.csv', encoding='utf-8')
data = pd.read_csv('微博清单_毛泽东旧居_前60页.csv', encoding='utf-8')
comments = data['微博内容']

# 加载中文词库和成语库
#jieba.load_userdict("custom_dict.txt")  # 可包含动词、名词、形容词等自定义词汇
with open('汉语成语词典_词表_23889条.txt', 'r', encoding='utf-8') as f:
    chengyu_list = f.read().splitlines()

# 统计函数
def extract_terms(text, term_type):
    """提取指定类型的词汇，并统计词频"""
    if term_type == '动词':
        terms = [word for word, flag in jieba.posseg.cut(text) if flag.startswith('v') and len(word) > 1]
    elif term_type == '名词':
        terms = [word for word, flag in jieba.posseg.cut(text) if flag.startswith('n') and len(word) > 1]
    elif term_type == '形容词':
        terms = [word for word, flag in jieba.posseg.cut(text) if flag.startswith('a') and len(word) > 1]
    elif term_type == '成语':
        terms = [word for word in jieba.cut(text) if word in chengyu_list and len(word) > 1]
    elif term_type == '四字词语':
        terms = [word for word in re.findall(r'\b\w{4}\b', text) if len(word) == 4]
    else:
        terms = []
    return terms

# 初始化计数器
verb_counter = Counter()
noun_counter = Counter()
adj_counter = Counter()
chengyu_counter = Counter()
four_char_counter = Counter()

# 遍历评论内容并统计词频
for comment in comments:
    verb_counter.update(extract_terms(comment, '动词'))
    noun_counter.update(extract_terms(comment, '名词'))
    adj_counter.update(extract_terms(comment, '形容词'))
    chengyu_counter.update(extract_terms(comment, '成语'))
    four_char_counter.update(extract_terms(comment, '四字词语'))

# 输出结果
print("动词词频：", verb_counter.most_common(10))
print("名词词频：", noun_counter.most_common(10))
print("形容词词频：", adj_counter.most_common(10))
print("成语词频：", chengyu_counter.most_common(10))
print("四字词语词频：", four_char_counter.most_common(10))

# 将统计结果导出到CSV文件
freq_df = pd.DataFrame({
    '动词': dict(verb_counter),
    '名词': dict(noun_counter),
    '形容词': dict(adj_counter),
    '成语': dict(chengyu_counter),
    '四字词语': dict(four_char_counter)
}).fillna(0)

freq_df.to_csv('_微博清单_毛泽东旧居_前60页.csv.csvterm_frequency_analysis.csv', encoding='utf-8-sig')
