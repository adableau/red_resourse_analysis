# -*- encoding:utf-8 -*-
from __future__ import print_function
import os
import json
import time
import sys

import gensim
import numpy as np
import time
import distance
import jieba.posseg as pesg
import sklearn
from sklearn import metrics

# 加载词向量
from sklearn.metrics import precision_recall_fscore_support
from sklearn.metrics import precision_recall_fscore_support

import dp_similarity
from nlp_util import file_utils


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


# 加入权重  tf_idf(word)  加到sum---
def tf_idf(s1, s2, word_list2):
    def add_space(s):
        return ' '.join(list(s))

    # 将字中间加入空格
    s1, s2 = add_space(s1), add_space(s2)
    # 转化为TF矩阵
    cv = sklearn.CountVectorizer(tokenizer=lambda s: s.split())
    corpus = [s1, s2]
    vectors = cv.fit_transform(corpus).toarray()
    # 求交集
    numerator = np.sum(np.min(vectors, axis=0))
    # 求并集
    denominator = np.sum(np.max(vectors, axis=0))
    # 计算杰卡德系数
    return 1.0 * numerator ** 2 / denominator


# 给予余弦相似度的相似度计算
def similarity_cosine(wv_from_text, word_list1, word_list2):
    vector1 = np.zeros(200)
    tf_idf_weight = tf_idf(word_list1, word_list2)
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

    similarity = tf_idf_weight * cos1 / float(cos21 * cos22)

    return similarity


def similarity_main(wv_from_text, comment, summary):
    # 测试句子相似度
    start_time = time.time()
    # vec_summary = wordVec(sentence_danmu1, wv_from_text, min_n=1, max_n=3)  # 词向量获取
    word_list1 = [word.word for word in pesg.cut(comment) if word.flag[0] not in ['w', 'x', 'u']]
    word_list2 = [word.word for word in pesg.cut(summary) if word.flag[0] not in ['w', 'x', 'u']]
    y = similarity_cosine(wv_from_text, word_list1, word_list2)
    print("------vec_similarity:", y)
    # print("----loading time:", time.time() - start_time)


def load_danmu(file_path):
    datas = []
    lines = open(file_path, 'r', encoding='utf8').read().strip().split('\n')
    for line in lines:
        data = json.loads(line)
        datas.append(data)
    return datas


def save_similarity_cosine(similarity_list, matrix_similarity_dir):
    wr = open(matrix_similarity_dir, 'w', encoding='utf8')
    wr.write(str(similarity_list))
    wr.close()


def dump_to_json(datas, fout):
    for data in datas:
        fout.write(json.dumps(data, sort_keys=True, separators=(',', ': '), ensure_ascii=False))
        fout.write('\n')
    fout.close()


# 1. 加载词向量
wv_from_text = gensim_vec()


def get_similarity(clean_summary_dir, clean_comment_cut_dir, matrix_similarity_dir):
    # 加载comment
    pathDir = os.listdir(clean_summary_dir)

    for idx, file_name_txt in enumerate(pathDir):
        y_true = []
        danmu_file = file_name_txt.split("_")
        danmu_file_path = os.path.join(clean_comment_cut_dir, danmu_file[0])
        origin_path = os.path.join(clean_summary_dir, file_name_txt)

        summary = file_utils.load_danmu(origin_path)
        danmu = file_utils.load_danmu(danmu_file_path)

        video_time_slice = []
        for i, n in enumerate(summary):
            video_time_slice.append(n["video"].split("-")[1])

        print(video_time_slice)

        datas = []
        danmu_file = file_name_txt.split("_")
        danmu_comment = danmu_file[2]
        if int(danmu_comment) != 0:
            danmu_file_path = os.path.join(clean_comment_cut_dir, danmu_file[0])

            if os.path.exists(danmu_file_path):
                danmu = load_danmu(danmu_file_path)

                origin_path = os.path.join(clean_summary_dir, file_name_txt)
                summary = load_danmu(origin_path)

                # n个剧情简介对应M块弹幕
                similarity_list = []
                for n in summary:
                    ps_init = 0
                    s_score = []
                    danmu_cut = ""
                    for m in danmu:
                        if ps_init == m["cut"]:
                            danmu_cut += " " + m["danmaku"]
                        else:
                            # todo 2. 计算句子相似度
                            # jjs = jaccard_similarity(danmu_cut, n["content"])
                            jjs = similarity_main(wv_from_text, danmu_cut, n["content"])
                            s_score.append(jjs)
                            ps_init += 1
                            danmu_cut = m["danmaku"]
                    similarity_list.append(s_score)


                    # 计算true lable
        cut_num_init = 0

        for m in danmu:
            cut_num = m["cut"]
            playtime = m["playtime"]

            for video_time_k, video_time_i in enumerate(video_time_slice, start=0):
                if int(playtime) < int(video_time_i):
                    label = video_time_k
                    break
            if cut_num != cut_num_init:
                y_true.append(label)
                cut_num_init = cut_num

        # if cut_num_init == ps_init:
        # 最后的cut
        #             y_true.append(len(video_time_slice) - 1)

        print(len(y_true))

        y_pred = dp_similarity.get_path(similarity_list)
        print(len(y_pred))

        acc = metrics.accuracy_score(y_true, y_pred)

        f1_score = metrics.f1_score(y_true, y_pred, average='weighted')
        macro_f1_score = metrics.f1_score(y_true, y_pred, average='macro')
        micro_f1_score = metrics.f1_score(y_true, y_pred, average='micro')
        # target_names = ['class 0', 'class 1', 'class 2']
        # score = metrics.classification_report(y_true, y_pred,target_names)
        macro_prf = precision_recall_fscore_support(y_true, y_pred, average='macro')
        micro_prf = precision_recall_fscore_support(y_true, y_pred, average='micro')
        weighted_prf = precision_recall_fscore_support(y_true, y_pred, average='weighted')
        # target_names = ['class 0', 'class 1', 'class 2']
        # score = metrics.classification_report(y_true, y_pred,target_names)

        print(acc)
        print(f1_score)
        print(macro_f1_score)
        print(micro_f1_score)
        print(macro_prf)
        # 保存相似度矩阵
        # matrix_similarity = os.path.join(matrix_similarity_dir, danmu_file)
        # save_similarity_cosine(similarity_list, matrix_similarity)
        print(danmu_file[0])
        datas.append({"acc": acc, "f1_score": str(f1_score), "weighted_prf": str(weighted_prf),
                      "micro_f1_score": str(micro_f1_score), "micro_prf": str(micro_prf), "macro_prf": str(macro_prf)
                      })

        matrix_similarity = os.path.join(matrix_similarity_dir, danmu_file[0] + "_cosin")
        file_utils.dump_to_json(datas, open(matrix_similarity, 'w', encoding='utf8'))

        # 保存相似度矩阵
        # matrix_similarity = os.path.join(matrix_similarity_dir, danmu_file)
        # save_similarity_cosine(similarity_list, matrix_similarity)
        # print(danmu_file[0])
        # datas.append({"danmu_file": danmu_file[0], "matrix_similarity": similarity_list})
        matrix_similarity = os.path.join(matrix_similarity_dir, danmu_file[0])
        save_similarity_cosine(similarity_list,
                               matrix_similarity)  # dump_to_json(datas, open(save_path, 'w', encoding='utf8'))
        print("---------finished---------")


if __name__ == '__main__':
    clean_comment_cut_dir = '../data/pairs/'
    clean_summary_dir = '../data/pairs/'
    matrix_similarity_dir = '../data/embeding_matrix_similarity/'

    # clean_comment_cut_dir = '/home/baiqingchun/0000/danmaku/data/clean_comment_cut_new/'
    # clean_summary_dir = '/home/baiqingchun/0000/danmaku/data/Entertainment_summary/'
    ##matrix_similarity_dir = '/home/baiqingchun/0000/danmaku/data/embeding_matrix_similarity/'

    # clean_comment_cut_dir = 'E:\danmu-201909\data.txt\clean_comment_cut_new/'
    # matrix_similarity_dir = 'E:\danmu-201909\embeding_matrix_similarity/'
    # clean_summary_dir = 'E:\danmu-201909\data.txt\Entertainment_summary/'

    # process_danmus(origin_comment_dir, clean_comment_dir, summary_dir)

    get_similarity(clean_summary_dir, clean_comment_cut_dir, matrix_similarity_dir)
