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


def get_corpus_dictionary():
    clean_comment_cut_dir = 'LDA/alltextold.txt'

    documents = file_utils.load_csv(clean_comment_cut_dir)

    stoplist = set('for a of the and to in'.split())

    texts = [[word for word in document if word not in stoplist]
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
    lda = LdaModel(corpus=corpus, num_topics=30)
    data = pyLDAvis.gensim.prepare(lda, corpus, dictionary)
    pyLDAvis.show(data, open_browser=False)


if __name__ == '__main__':
    test_lda()
