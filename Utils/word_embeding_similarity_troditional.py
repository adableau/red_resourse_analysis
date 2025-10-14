# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 30 09:35:54 2018

@author: Administrator
"""

import jieba
import numpy as np


def get_word_vector():
    """
    w = np.ones((3,4))
    q = np.ones((3,4"))
    print(w)
    print(np.sum(w * q))
   """

    sentence_danmu1 = "她 爹姓 什么 不是 应该 跟 爹性 么 ？说好 的 世间 最后 一个 神呐 , 不 随爹 姓 哈哈哈 ,花千骨好漂亮呀"
    sentence_danmu2 = "差点被弹幕的十年后给骗了.十年 修 得 白子 画 百年 修得 霍 建华。 啊 ？ 才 十六年 ！ π _ π "
    sentence_sumarry = "花莲村忽生异香百花枯萎，蜀山掌门清虚道长发现这一切皆因一名女婴，他赠衣服相助之余为其取名花千骨。"
    sentence_sumarry2 = "十六年后，小骨在找大夫医治父亲时遭到妖魔袭击，危急之时长留上仙白子画化名墨冰挺身相救，花父不久后命丧黄泉。"

    s1 = input(sentence_danmu1)
    s2 = input(sentence_sumarry)

    cut1 = jieba.cut(s1)
    cut2 = jieba.cut(s2)

    list_word1 = (','.join(cut1)).split(',')
    list_word2 = (','.join(cut2)).split(',')
    print(list_word1)
    print(list_word2)

    key_word = list(set(list_word1 + list_word2))  # 取并集
    print(key_word)

    word_vector1 = np.zeros(len(key_word))  # 给定形状和类型的用0填充的矩阵存储向量
    word_vector2 = np.zeros(len(key_word))

    for i in range(len(key_word)):  # 依次确定向量的每个位置的值
        for j in range(len(list_word1)):  # 遍历key_word中每个词在句子中的出现次数
            if key_word[i] == list_word1[j]:
                word_vector1[i] += 1
        for k in range(len(list_word2)):
            if key_word[i] == list_word2[k]:
                word_vector2[i] += 1

    print(word_vector1)  # 输出向量
    print(word_vector2)
    return word_vector1, word_vector2


def cosine():
    v1, v2 = get_word_vector()
    return float(np.sum(v1 * v2)) / (np.linalg.norm(v1) * np.linalg.norm(v2))


print(cosine())
