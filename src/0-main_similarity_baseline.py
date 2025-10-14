# -*- encoding:utf-8 -*-
import os

from sklearn import metrics
from sklearn.metrics import precision_recall_fscore_support
import numpy as np
import file_utils


def get_similarity(method, clean_summary_dir, clean_comment_cut_dir, matrix_similarity_dir):
    # 加载comment
    pathDir = os.listdir(clean_summary_dir)

    resu = []
    all_P, all_R, all_F ,all_F2= 0, 0, 0,0
    # 1. 加载词向量
    # wv_from_text = similarity.gensim_vec()
    for idx, file_name_txt in enumerate(pathDir):
        y_true = []
        y_pred = []
        datas = []

        danmu_file = file_name_txt.split("_")
        danmu_file_path = os.path.join(clean_comment_cut_dir, danmu_file[0])
        origin_path = os.path.join(clean_summary_dir, file_name_txt)

        summary = file_utils.load_danmu(origin_path)
        danmu = file_utils.load_danmu(danmu_file_path)

        video_time_slice = []
        for i, n in enumerate(summary):
            video_time_slice.append(n["video"].split("-")[1])

        print(video_time_slice)
        ps_init = 0
        cut_num_init = 0
        # n个剧情简介对应M块弹幕
        similarity_list = []
        danmu_cut_len = len(danmu)
        summary_cut_len = len(summary)
        # 均分,每一份长度
        cut_num = int(danmu_cut_len / summary_cut_len)

        for i, m in enumerate(danmu):
            cut_true = m["cut"]
            if ps_init != cut_true:
                y_pred.append(int(i / cut_num))
                ps_init = cut_true

        for m in danmu:
            playtime = m["playtime"]
            cut_true = m["cut"]
            for video_time_k, video_time_i in enumerate(video_time_slice, start=0):
                if int(playtime) < int(video_time_i):
                    label = video_time_k
                    break
            if cut_true != cut_num_init:
                y_true.append(label)
                cut_num_init = cut_true

        # if cut_num_init == ps_init:
        # 最后的cut
        #             y_true.append(len(video_time_slice) - 1)

        print("---------")
        print(len(y_true))
        correct_sum = 0
        # y_pred.extend(dp_similarity.get_path(similarity_list))
        print(len(y_pred))
        for k in range(len(y_pred)):
            if y_true[k] == y_pred[k]:
                correct_sum += 1
        correct_predictions = float(np.mean(y_true == y_pred))

        print({"correct_predictions":correct_predictions})
        p = metrics.precision_score(y_true, y_pred, average='weighted')
        macro_f1_score = metrics.f1_score(y_true, y_pred, average='macro')
        micro_f1_score = metrics.f1_score(y_true, y_pred, average='micro')
        macro_prf = precision_recall_fscore_support(y_true, y_pred, average='weighted')
        # target_names = ['class 0', 'class 1', 'class 2']
        # score = metrics.classification_report(y_true, y_pred,target_names)
        # weighted_prf = precision_recall_fscore_support(y_true, y_pred, average='weighted')
        # target_names = ['class 0', 'class 1', 'class 2']
        # score = metrics.classification_report(y_true, y_pred,target_names)

        print(p)
        print(macro_f1_score)
        print(micro_f1_score)
        # 保存相似度矩阵
        # matrix_similarity = os.path.join(matrix_similarity_dir, danmu_file)
        # save_similarity_cosine(similarity_list, matrix_similarity)
        print(danmu_file[0])


        LEN = len(pathDir)+1
        P, R, F = macro_prf[0], macro_prf[1], macro_prf[2]
        F2 = 2 * P * R / (P + R)
        all_P += P
        all_R += R
        all_F += F
        all_F2 += F2
        resu.append({"P": str(P), "R": str(R), "F": str(F2), "macro_F": str(F)})


    # 保存相似度矩阵
    # matrix_similarity = os.path.join(matrix_similarity_dir, danmu_file)
    # save_similarity_cosine(similarity_list, matrix_similarity)
    # print(danmu_file[0])
    resu.append({"P": str(all_P /LEN ), "R": str(all_R / LEN), "F": str(all_F2 / LEN),
                 "macro_F": str(all_F / LEN)})
    datas.append(resu)
    matrix_similarity = os.path.join(matrix_similarity_dir, "baseline")
    file_utils.dump_to_json(datas, open(matrix_similarity, 'w', encoding='utf8'))

print("---------finished---------")

if __name__ == '__main__':
    # clean_comment_cut_dir = '../data/clean_comment_cut/'
    # clean_summary_dir = '../data/Entertainment_summary/'
    # clean_comment_cut_dir = 'E:\danmu-201909\data.txt\clean_comment_cut_new/'

    # clean_comment_cut_dir = 'E:\danmu-201909\data.txt/0923-clean_comment_cut_new'
    # clean_summary_dir = 'E:\danmu-201909\data.txt\Entertainment_summary/'
    # matrix_similarity_dir = 'E:\danmu-201909\data.txt/matrix_similarity/'

    clean_comment_cut_dir = '../data/pairs/danmaku'
    clean_summary_dir = '../data/pairs/summary'
    matrix_similarity_dir = '../data/embeding_matrix_similarity/'
    method = "jaccard_similarity"

    get_similarity(method, clean_summary_dir, clean_comment_cut_dir, matrix_similarity_dir)
