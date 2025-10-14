# coding:utf-8  
import os
import sys
from sklearn import feature_extraction
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer

import sys

try:
    sys.reload(sys)
    sys.setdefaultencoding('utf-8')
except:
    pass

import jieba
import jieba.posseg as pseg

jieba.load_userdict("backlist.txt")

#save_vacob_voc = 'vocab.danmaku.txt'
save_file_voc = 'file.tweeter18.txt'
open_file = '../data/input/tweeter14'

word_type = ["x", "zg"]


# 创建停用词list
def stopwordslist(filepath):
    stopwords = [line.strip() for line in open(filepath, 'r').readlines()]
    return stopwords


# 分词
def jieba_cutwords(open_cut_file):
    corpus = []
    # stopwords = stopwordslist('stopwords.txt')  # 这里加载停用词的路径
    # fw = open(save_file_voc, 'w')
    remove_words_list = []
    for line in open_cut_file:
        words = pseg.cut(line)
        remove_words = ''
        for w in words:
            # if w.encode("utf-8").decode('utf-8') not in stopwords:
            # print(w.word)
            if w.flag not in word_type:
                # print('{0} {1}'.format(w.word, w.flag))
                # print(type(w.word))  # in py2 is unicode, py3 is str
                remove_words = remove_words + ' ' + str(w.word)
        # corpus.append(remove_words)
        # fw.write(remove_words)
        # fw.write("\n")
        remove_words_list.append(remove_words)
    return remove_words_list


if __name__ == "__main__":

    # todo replace
    pathDir = os.listdir(open_file)
    # 将弹幕切词文件写到这儿
    remove_words_list = []
    save_file = open(save_file_voc, 'w')
    #file_voc = open(save_vacob_voc, 'w')
    indexi = 1
    word_index = 0
    mp = dict()  # 存放词频
    for path in pathDir:
        onefile = open(open_file + "/" + path, 'r').readlines()
        corpus = jieba_cutwords(onefile)
        # corpus = open(save_file_voc, 'r').read()
        vectorizer = CountVectorizer()  # 该类会将文本中的词语转换为词频矩阵，矩阵元素a[i][j] 表示j词在i类文本下的词频
        transformer = TfidfTransformer()  # 该类会统计每个词语的tf-idf权值
        tfidf = transformer.fit_transform(
            vectorizer.fit_transform(corpus))  # 第一个fit_transform是计算tf-idf，第二个fit_transform是将文本转为词频矩阵
        word = vectorizer.get_feature_names()  # 获取词袋模型中的所有词语
        weight = tfidf.toarray()  # 将tf-idf矩阵抽取出来，元素a[i][j]表示j词在i类文本中的tf-idf权重

        for i in range(len(weight)):  # 打印每类文本的tf-idf词语权重，第一个for遍历所有文本，第二个for便利某一类文本下的词语权重
            for j in range(len(word)):
                if weight[i][j] > 0:
                    # todo ave_file.write('{0} {1} {2}'.format(indexi, word[j], weight[i][j]))
                    save_file.write('{0} {1} {2}'.format(i , word[j], weight[i][j]))
                    save_file.write("\n")
                    # 存储到词表
        for w in word:
            word_index += 1
            mp[word_index] = w

            # print w.encode("utf-8").decode('utf-8')

        indexi += 1

