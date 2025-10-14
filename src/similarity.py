# -*- encoding:utf-8 -*-
"""
@author:   Qingchun Bai
"""

import gensim
import numpy as np
import time
import distance
import jieba.posseg as pesg


# 加载词向量
def gensim_vec():
    print("----start load vec------")
    start_time = time.time()
    wv_from_text = gensim.models.KeyedVectors.load_word2vec_format('Tencent_AILab_ChineseEmbedding.txt', binary=False)
    wv_from_text.init_sims(replace=True)  # 神奇，很省内存，可以运算most_similar
    print("----loading time:", time.time() - start_time)
    return wv_from_text


# 计算word的ngrams词组
def compute_ngrams(word, min_n, max_n):
    # BOW, EOW = ('<', '>')  # Used by FastText to attach to all words as prefix and suffix
    extended_word = word
    ngrams = []
    for ngram_length in range(min_n, min(len(extended_word), max_n) + 1):
        for i in range(0, len(extended_word) - ngram_length + 1):
            ngrams.append(extended_word[i:i + ngram_length])
    return list(set(ngrams))


# 不在词典的情况下,计算相近向量
def word_vec(word, wv_from_text, min_n=1, max_n=3):
    # 确认词向量维度
    word_size = wv_from_text.wv.syn0[0].shape[0]
    # 计算word的ngrams词组
    ngrams = compute_ngrams(word, min_n=min_n, max_n=max_n)
    # 如果在词典之中，直接返回词向量
    if word in wv_from_text.index2word:
        global found
        found += 1
        return wv_from_text[word]
    else:
        # 不在词典的情况下，计算与词相近的词向量
        word_vec = np.zeros(word_size, dtype=np.float32)
        ngrams_found = 0
        ngrams_single = [ng for ng in ngrams if len(ng) == 1]
        ngrams_more = [ng for ng in ngrams if len(ng) > 1]
        # 先只接受2个单词长度以上的词向量
        for ngram in ngrams_more:
            if ngram in wv_from_text.index2word:
                word_vec += wv_from_text[ngram]
                ngrams_found += 1
                # print(ngram)
        # 如果，没有匹配到，那么最后是考虑单个词向量
        if ngrams_found == 0:
            for ngram in ngrams_single:
                if ngram in wv_from_text.index2word:
                    word_vec += wv_from_text[ngram]
                    ngrams_found += 1
        if word_vec.any():  # 只要有一个不为0
            return word_vec / max(1, ngrams_found)
        else:
            print('all ngrams for word %s absent from model' % word)
            return 0


# 给予余弦相似度的相似度计算
def similarity_cosine(wv_from_text, word_list1, word_list2):
    vector1 = np.zeros(200)
    # 如果在词典之中，直接返回词向量
    for word in word_list1:
        vector1 += word_vec(word, wv_from_text)
    vector1 = vector1 / len(word_list1)
    # print(vector1)
    vector2 = np.zeros(200)
    for word in word_list2:
        vector2 += word_vec(word, wv_from_text)
    vector2 = vector2 / len(word_list2)
    # print(vector2)
    cos1 = np.sum(vector1 * vector2)
    cos21 = np.sqrt(sum(vector1 ** 2))
    cos22 = np.sqrt(sum(vector2 ** 2))
    similarity = cos1 / float(cos21 * cos22)
    return similarity


def similarity_main(wv_from_text, comment, summary):
    # 测试句子相似度
    start_time = time.time()
    # vec_summary = wordVec(sentence_danmu1, wv_from_text, min_n=1, max_n=3)  # 词向量获取
    word_list1 = [word.word for word in pesg.cut(comment) if word.flag[0] not in ['w', 'x', 'u']]
    word_list2 = [word.word for word in pesg.cut(summary) if word.flag[0] not in ['w', 'x', 'u']]
    y = similarity_cosine(wv_from_text, word_list1, word_list2)
    print("------vec_similarity:", y)
    print("----loading time:", time.time() - start_time)


from sklearn.feature_extraction.text import CountVectorizer




if __name__ == '__main__':
    sentence_danmu1 = "她爹姓什么不应该跟爹性么 ？说好的世间最后 一个神呐 , 不随爹姓哈哈哈 ,花千骨好漂亮呀"
    sentence_danmu2 = "差点被弹幕的十年后给骗了.十年 修 得 白子 画 百年 修得 霍 建华。 啊 ？ 才 十六年 ！ π _ π "
    sentence_danmu3 = "你们 知不知道 这个 老头 的 演员 是 个 很 新潮 的 人 清微 老头 呢 "
    sentence_summary = "花莲村忽生异香百花枯萎，蜀山掌门清虚道长发现这一切皆因一名女婴，他赠衣服相助之余为其取名花千骨。"
    sentence_summary2 = "十六年后，小骨在找大夫医治父亲时遭到妖魔袭击，危急之时长留上仙白子画化名墨冰挺身相救，花父不久后命丧黄泉。"
    # 1. 加载词向量
    #wv_from_text = gensim_vec()
    # 2. 计算句子相似度
    #similarity_main(wv_from_text, sentence_danmu1, sentence_summary)

    word_list1 = [word.word for word in pesg.cut(sentence_danmu1) if word.flag[0] not in ['w', 'x', 'u']]
    word_list2 = [word.word for word in pesg.cut(sentence_summary) if word.flag[0] not in ['w', 'x', 'u']]

    print(jaccard_similarity(word_list1,word_list2))
