# -*- encoding:utf-8 -*-
import pyLDAvis.gensim
from gensim import corpora
from gensim.models import LdaModel

import os

from sklearn import metrics
from sklearn.metrics import precision_recall_fscore_support

import dp_similarity
import file_utils
import jaccard_similarity as jsm


def get_danmu(method, clean_summary_dir, clean_comment_cut_dir, matrix_similarity_dir):
    # 加载comment
    pathDir = os.listdir(clean_summary_dir)
    danmu_doc=[]
    # 1. 加载词向量
    # wv_from_text = similarity.gensim_vec()
    for idx, file_name_txt in enumerate(pathDir):
        datas = []
        y_true = []
        danmu_file = file_name_txt.split("_")
        danmu_file_path = os.path.join(clean_comment_cut_dir, danmu_file[0])
        origin_path = os.path.join(clean_summary_dir, file_name_txt)
        danmu_cut=""
        #summary = file_utils.load_danmu(origin_path)
        danmu = file_utils.load_danmu(danmu_file_path)
        for m in danmu:
            danmu_cut += " " + m["danmaku_clean"]
        danmu_doc.append(danmu_cut)
    return danmu_doc

def get_corpus_dictionary():
    clean_comment_cut_dir = '../data/pairs/danmaku'
    clean_summary_dir = '../data/pairs/summary'
    matrix_similarity_dir = '../data/embeding_matrix_similarity/'
    method = "jaccard_similarity"

    documents =get_danmu(method, clean_summary_dir, clean_comment_cut_dir, matrix_similarity_dir)

    stoplist = set('for a of the and to in'.split())
    texts = [[word for word in document.lower().split() if word not in stoplist]
             for document in documents]

    from collections import defaultdict
    frequency = defaultdict(int)
    for text in texts:
        for token in text:
            frequency[token] += 1

    texts = [[token for token in text if frequency[token] > 1]
             for text in texts]
    dictionary = corpora.Dictionary(texts)
    corpus = [dictionary.doc2bow(text) for text in texts]

    return corpus, dictionary

def test_lda():
    corpus, dictionary = get_corpus_dictionary()
    lda = LdaModel(corpus=corpus,num_topics=10)
    data = pyLDAvis.gensim.prepare(lda, corpus, dictionary)
    pyLDAvis.show(data,open_browser=False)

if __name__ == '__main__':
    test_lda()

