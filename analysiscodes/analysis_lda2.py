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


import pandas as pd

# 定义主题模型数据
data = {
    "Topic": [
        "Topic 0", "Topic 1", "Topic 2", "Topic 3",
        "Topic 4", "Topic 5", "Topic 6", "Topic 7",
        "Topic 8", "Topic 9"
    ],
    "Keywords": [
        "红色旅游专列, 千城一面, 上海红色旅游宣传大使, 不止旅行, 刘小锋, 慢节奏, 上海旅行, 旅行, 新浪旅游, 春节休闲去哪玩",
        "上海, 开天辟地, 走向未来, 英烈丰碑, 文化先驱, 伟人风范, 新时代重走一大路, 嘉兴身边事, 六安号, 景点",
        "乐游上海,坐着火车, 中共一大纪念馆, 共话山海情, 十条红色微旅行线路, 上海全面提升红色旅游发展水平, 打卡网红汉堡店, 拍照合适的不得了",
        "发展华中, 宝安新苑党总支, 中央决策, 俞善进, 健儿与国民党硕固派韩德勤率领的, 东进黄桥, 握苏北, 新四军歼灭顽军, 乐游长三角, 六安号",
        "红色旅游, 红色旅游进校园, 吉安号, 五好, 陕西省旅游发展委员会,  一大, 四史, 沙家浜一日游, 西安发布",
        "重走一大路, 上海三明周末游, 六安, 六安号, 建党百年, 百条精品线路,  嘉兴发布, 田埂工作室, 三明文旅",
        "沪浙红色旅游区, 劉長勝故居, 初心之地, 的主题形象是, 智慧粮仓, 深圳市民从, 洋网红, 未来之都, 微实事, 大变化",
        "上海三明周末游, 上海嘉兴,旅游专列, 复古列车,恢复开行, 上海嘉兴红色旅游列车, 向未来, 上海政法学院, 沪明情, 党的诞生地, 享受",
        "在路上看中国, 周恩来号, 火车邮局, 党史学习角, 一江一河, 上海至嘉兴, 建党百年红色旅游百条精品线路, 湘沪相邀, 初心闪耀, 火星人",
        "网页链接, 七一, 夜上海,  小上海, 粉红色圈套, 建筑可阅读, 美篇, 转载"
    ]
}

# 创建DataFrame
df_topics = pd.DataFrame(data)

# 显示DataFrame
print(df_topics)

# 保存到CSV文件
df_topics.to_csv("topics_keywords_table2.csv", index=False)
print("主题关键词表已成功保存为 'topics_keywords_table.csv'")

