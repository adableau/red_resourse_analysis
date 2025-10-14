import math
import jieba

from gensim.summarization import bm25
from gensim.summarization.textcleaner import get_sentences, split_sentences

from data_utils import *

# 测试文本
text = '''
自然语言处理是计算机科学领域与人工智能领域中的一个重要方向。
它研究能实现人与计算机之间用自然语言进行有效通信的各种理论和方法。
自然语言处理是一门融语言学、计算机科学、数学于一体的科学。
因此，这一领域的研究将涉及自然语言，即人们日常使用的语言，
所以它与语言学的研究有着密切的联系，但又有重要的区别。
自然语言处理并不是一般地研究自然语言，
而在于研制能有效地实现自然语言通信的计算机系统，
特别是其中的软件系统。因而它是计算机科学的一部分。
'''


class BM25(object):
    def __init__(self, docs):
        self.D = len(docs)
        self.avgdl = sum([len(doc) + 0.0 for doc in docs]) / self.D
        self.docs = docs
        self.f = []  # 列表的每一个元素是一个dict，dict存储着一个文档中每个词的出现次数
        self.df = {}  # 存储每个词及出现了该词的文档数量
        self.idf = {}  # 存储每个词的idf值
        self.k1 = 1.5
        self.b = 0.75
        self.init()

    def init(self):
        for doc in self.docs:
            tmp = {}
            for word in doc:
                tmp[word] = tmp.get(word, 0) + 1  # 存储每个文档中每个词的出现次数
            self.f.append(tmp)
            for k in tmp.keys():
                self.df[k] = self.df.get(k, 0) + 1
        for k, v in self.df.items():
            self.idf[k] = math.log(self.D - v + 0.5) - math.log(v + 0.5)

    def sim(self, doc, index):  # score
        score = 0
        for word in doc:
            if word not in self.f[index]:
                continue
            d = len(self.docs[index])
            score += (self.idf[word] * self.f[index][word] * (self.k1 + 1)
                      / (self.f[index][word] + self.k1 * (1 - self.b + self.b * d
                                                          / self.avgdl)))
        return score

    def simall(self, doc):
        scores = []
        for index in range(self.D):
            score = self.sim(doc, index)
            scores.append(score)
        return scores

    def simlarity_scores(self, doc):
        scores = []
        for index in range(self.D):
            score = self.sim(doc, index)
            scores.append(score)
        return scores


def cal_bm25_sim(bm25Model, tokens1, tokens2):
    ts1, ts2 = tokens1, tokens2
    if len(tokens1) > len(tokens2):
        ts1 = tokens2
        ts2 = tokens1
    freqs = {}
    for word in ts2:
        if word not in freqs:
            freqs[word] = 0
        freqs[word] += 1

    param_k1 = 1.5
    param_b = 0.75
    score1, score2 = 0.0, 0.0
    for word in ts1:
        if word not in freqs or word not in bm25Model.idf:
            continue
        score1 += (bm25Model.idf[word] * freqs[word] * (param_k1 + 1) / (
            freqs[word] + param_k1 * (1 - param_b + param_b * 1)))
    for word in ts2:
        if word not in freqs or word not in bm25Model.idf:
            continue
        score2 += (bm25Model.idf[word] * freqs[word] * (param_k1 + 1) / (
            freqs[word] + param_k1 * (1 - param_b + param_b * 1)))
    #print(score1)
    #print(score2)
    score2 = score2 if score2>0 else 1
    sim = score1 / score2
    sim = sim if sim <= 1.0 else 1.0
    return sim


if __name__ == '__main__':
    sents = split_sentences(text)
    doc = []
    for sent in sents:
        words = list(jieba.cut(sent))
        # words = filter_stop(words)
        doc.append(words)
    print(doc)
    bm_model = bm25.BM25(doc)
    ##print(s.f)
    # print(s.idf)
    print("-------------")

    print(cal_bm25_sim(bm_model, "人能", '人工智能计算机科学'))
    # print(bm_model.simall(['自然语言', '计算机科学', '领域', '人工智能', '领域']))
    # print(bm_model.simall("人工智能"))
    print("-------------")
