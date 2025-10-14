# -*- encoding:utf-8 -*-
import numpy as np
from nlp_util import file_utils
import os


def get_path(matrix_data):
    mas = np.array(matrix_data)
    m = len(matrix_data)  # 4
    n = len(matrix_data[0])  # 5
    dp = np.zeros((m + 1, n + 1), dtype=np.float)  # 记录值
    path = np.zeros((m, n), dtype=np.int)  # 路径
    dp[0][0] = mas[0][0]

    sum_list = np.array(matrix_data)
    sum_list[0][0] = mas[0][0]
    for i in range(m):
        for j in range(n):
            if i == 0 and j == 0:  # 左上角
                sum_list[i][j] = matrix_data[i][j]
            elif i == 0:  # 第一行 i=0
                sum_list[i][j] = matrix_data[i][j] + sum_list[i][j - 1]
            elif j == 0:  # 第一列 i=0
                sum_list[i][j] = matrix_data[i][j] + sum_list[i - 1][j]
            else:  # 其他情况
                sum_1 = matrix_data[i][j] + sum_list[i - 1][j]  # 上边过来
                sum_2 = matrix_data[i][j] + sum_list[i][j - 1]  # 左边过来
                if sum_1 > sum_2:  # 上边大于左边
                    sum_list[i][j] = sum_1
                else:  # 上边不大于左边
                    sum_list[i][j] = sum_2
    print(sum_list)
    #Path(state sequence) backtracking
    i = m - 1
    j = n - 1
    path[i][j] = 1
    while (j != 0 and i != 0):
        sum_1 = sum_list[i - 1][j]  # 上边da
        sum_2 = sum_list[i][j - 1]  # 左边da
        if sum_1 > sum_2:  # 上边大于左边
            path[i - 1][j] = 1
            path[i][j - 1] = 0
            i = i - 1
        else:  # 上边不大于左边
            path[i][j - 1] = 1
            path[i - 1][j] = 0
            j = j - 1
    while (i == 0 and j != 0):
        path[i][j - 1] = 1
        j = j - 1
    while (j == 0 and i != 0):
        path[i - 1][j] = 1
        i = i - 1
    path[0][0] = 1
    print(path)
    print("-----------")
    return path.argmax(axis=0)


def get_matrix_similarity(matrix_similarity_dir):
    matrix_similarity = file_utils.load_from_json(open(matrix_similarity_dir, 'r', encoding='utf8'))
    print(matrix_similarity)
    # return np.mat(matrix_similarity)
    return matrix_similarity


if __name__ == '__main__':
    clean_comment_cut_dir = '../data/pairs/danmaku'
    clean_summary_dir = '../data/pairs/summary'
    matrix_similarity_dir = '../data/embeding_matrix_similarity/'
    pathDir = os.listdir(matrix_similarity_dir)  # 文件夹下所有
