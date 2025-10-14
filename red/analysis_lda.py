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
import pandas as pd
import gensim
import gensim.corpora as corpora
from gensim.models import LdaModel
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import nltk; nltk.download('stopwords'); nltk.download('punkt')


# 加载数据
#file_path = '3redsourse_combined_weibo_data.csv'
file_path = '微博清单_上海红色故事_前50页.csv'
df = pd.read_csv(file_path)

# 数据预处理
# 假设微博内容在列 '微博内容'
texts = df['微博内容'].dropna().map(lambda x: word_tokenize(x.lower()))
stop_words = set(stopwords.words('chinese'))  # 请确保这里使用正确的语言
texts = [[word for word in doc if word not in stop_words and word.isalpha()] for doc in texts]

# 创建字典和语料库
id2word = corpora.Dictionary(texts)
corpus = [id2word.doc2bow(text) for text in texts]

# 构建LDA模型
num_topics = 10  # 可以根据需要调整主题数量
lda_model = LdaModel(corpus=corpus,
                     id2word=id2word,
                     num_topics=num_topics,
                     random_state=100,
                     update_every=1,
                     chunksize=100,
                     passes=10,
                     alpha='auto')

# 显示主题
for idx, topic in lda_model.print_topics(-1):
    print('Topic: {} \nWords: {}'.format(idx, topic))
