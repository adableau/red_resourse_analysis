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
from models import dtw
from nlp_util import data_utils

if __name__ == '__main__':

    matrix_similarity_dir = '../data/embeding_matrix_similarity/'

    # 加载comment
    pathDir = os.listdir(matrix_similarity_dir)
    for idx, file_name_txt in enumerate(pathDir):
        origin_path = os.path.join(matrix_similarity_dir, file_name_txt)
        matrix = data_utils.read_data(origin_path)

        print(matrix)
        arr = np.array(matrix)

        dtw.display(arr[0], arr[1])

        print("----finsish-----%s", file_name_txt)
