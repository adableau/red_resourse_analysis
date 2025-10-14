import gensim
import numpy as np
import time
import distance
import jieba.posseg as pesg


# 数据集格式化加载。。。

# load_embedding('Tencent_AILab_ChineseEmbedding.txt')

def gensim_vec():
    print("----start load vec------")
    start_time = time.time()
    wv_from_text = gensim.models.KeyedVectors.load_word2vec_format('Tencent_AILab_ChineseEmbedding.txt', binary=False)
    wv_from_text.init_sims(replace=True)  # 神奇，很省内存，可以运算most_similar
    print("----loading time:", time.time() - start_time)
    return wv_from_text


def compute_ngrams(word, min_n, max_n):
    # BOW, EOW = ('<', '>')  # Used by FastText to attach to all words as prefix and suffix
    extended_word = word
    ngrams = []
    for ngram_length in range(min_n, min(len(extended_word), max_n) + 1):
        for i in range(0, len(extended_word) - ngram_length + 1):
            ngrams.append(extended_word[i:i + ngram_length])
    return list(set(ngrams))


def wordVec(word, wv_from_text, min_n=1, max_n=3):
    '''
    ngrams_single/ngrams_more,主要是为了当出现oov的情况下,最好先不考虑单字词向量
    '''
    # 确认词向量维度
    word_size = wv_from_text.wv.syn0[0].shape[0]
    # 计算word的ngrams词组
    ngrams = compute_ngrams(word, min_n=min_n, max_n=max_n)
    # 如果在词典之中，直接返回词向量
    if word in wv_from_text.wv.vocab.keys():
        return wv_from_text[word]
    else:
        # 不在词典的情况下
        word_vec = np.zeros(word_size, dtype=np.float32)
        ngrams_found = 0
        ngrams_single = [ng for ng in ngrams if len(ng) == 1]
        ngrams_more = [ng for ng in ngrams if len(ng) > 1]
        # 先只接受2个单词长度以上的词向量
        for ngram in ngrams_more:
            if ngram in wv_from_text.wv.vocab.keys():
                word_vec += wv_from_text[ngram]
                ngrams_found += 1
                # print(ngram)
        # 如果，没有匹配到，那么最后是考虑单个词向量
        if ngrams_found == 0:
            for ngram in ngrams_single:
                word_vec += wv_from_text[ngram]
                ngrams_found += 1
        if word_vec.any():
            return word_vec / max(1, ngrams_found)
        else:
            raise KeyError('all ngrams for word %s absent from model' % word)


def similarity_cosine(wv_from_text, word_list1, word_list2):  # 给予余弦相似度的相似度计算
    vector1 = np.zeros(200)

    # 如果在词典之中，直接返回词向量
    for word in word_list1:
        vector1 += wordVec(word)
    vector1 = vector1 / len(word_list1)
    vector2 = np.zeros(200)
    for word in word_list2:
        vector2 += wordVec(word)
    vector2 = vector2 / len(word_list2)
    cos1 = np.sum(vector1 * vector2)
    cos21 = np.sqrt(sum(vector1 ** 2))
    cos22 = np.sqrt(sum(vector2 ** 2))
    similarity = cos1 / float(cos21 * cos22)
    return similarity


# '''计算句子相似度'''
def sim_distance(wv_from_text, text1, text2):  # 相似性计算主函数
    word_list1 = [word.word for word in pesg.cut(text1) if word.flag[0] not in ['w', 'x', 'u']]
    word_list2 = [word.word for word in pesg.cut(text2) if word.flag[0] not in ['w', 'x', 'u']]
    return similarity_cosine(wv_from_text, word_list1, word_list2)


def edit_distance(s1, s2):
    return distance.levenshtein(s1, s2)


from sklearn.feature_extraction.text import CountVectorizer


def jaccard_similarity(s1, s2):
    def add_space(s):
        return ' '.join(list(s))

    # 将字中间加入空格
    s1, s2 = add_space(s1), add_space(s2)
    # 转化为TF矩阵
    cv = CountVectorizer(tokenizer=lambda s: s.split())
    corpus = [s1, s2]
    vectors = cv.fit_transform(corpus).toarray()
    # 求交集
    numerator = np.sum(np.min(vectors, axis=0))
    # 求并集
    denominator = np.sum(np.max(vectors, axis=0))
    # 计算杰卡德系数
    return 1.0 * numerator / denominator


sentence_danmu1 = "她 爹姓 什么 不是 应该 跟 爹性 么 ？说好 的 世间 最后 一个 神呐 , 不 随爹 姓 哈哈哈 ,花千骨好漂亮呀"
sentence_danmu2 = "差点被弹幕的十年后给骗了.十年 修 得 白子 画 百年 修得 霍 建华。 啊 ？ 才 十六年 ！ π _ π "
sentence_danmu3 = "你们 知不知道 这个 老头 的 演员 是 个 很 新潮 的 人 清微 老头 呢 "
sentence_sumarry = "花莲村忽生异香百花枯萎，蜀山掌门清虚道长发现这一切皆因一名女婴，他赠衣服相助之余为其取名花千骨。"
sentence_sumarry2 = "十六年后，小骨在找大夫医治父亲时遭到妖魔袭击，危急之时长留上仙白子画化名墨冰挺身相救，花父不久后命丧黄泉。"

print("------edit_distance--------------")
results = list(filter(lambda x: edit_distance(x, sentence_danmu1) <= 2, sentence_sumarry))
print(results)

print("------jaccard_similarity--------------")
print(jaccard_similarity(sentence_danmu3, sentence_sumarry2))

print("------gensim-----------------------")

wv_from_text = gensim_vec()
vec_danmu = wordVec(sentence_danmu1, wv_from_text, min_n=1, max_n=3)  # 词向量获取
print(wv_from_text.most_similar(positive=[vec_danmu], topn=10))  # 相似词查找

print("------vec_similarity--------------")
# 测试句子相似度
start_time = time.time()
vec_sumarry = wordVec(sentence_danmu1, wv_from_text, min_n=1, max_n=3)  # 词向量获取
y = sim_distance(wv_from_text, vec_danmu, vec_sumarry)
print(y)
print("----loading time:", time.time() - start_time)
