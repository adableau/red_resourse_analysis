# -*- encoding:utf-8 -*-
from __future__ import print_function
from textrank4zh import TextRank4Keyword, TextRank4Sentence

from file_utils import read_txtfile


def extract_comment(origin_comment_dir, result_path):
    with open(result_path, 'w', encoding='utf-8') as fw:
        danmus = read_txtfile(origin_comment_dir)

        tr4w = TextRank4Keyword()
        tr4w.analyze(text=danmus, lower=True, window=2)  # py2中text必须是utf8编码的str或者unicode对象，py3中必须是utf8编码的bytes或者str对象

        tr4s = TextRank4Sentence()
        tr4s.analyze(text=danmus, lower=True, source='all_filters')
        fw.write('关键句子：' + '\n')
        for item in tr4s.get_key_sentences(num=5):
            # print(round(item.weight*10000, 2), item.sentence)
            fw.write("%s\t%s\n" % (float(round(item.weight, 3)), item.sentence))
            fw.write('\n')
        print("----finished------")


if __name__ == '__main__':
    # origin_file_dir = '../data/origin_barrage/3/'
    # clean_file_dir = '../data/clean_barrage/3/'
    # extract_barrage(origin_file_dir, clean_file_dir)

    origin_comment_dir = '上海红色旅游text.txt'
    result_path = 'res1.txt'
    extract_comment(origin_comment_dir, result_path)
