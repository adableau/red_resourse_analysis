# -*- encoding:utf-8 -*-
import os

from sklearn import metrics
from sklearn.metrics import precision_recall_fscore_support

import dp_similarity
import file_utils
import jaccard_similarity as jsm

import numpy as np


def get_similarity2(method, clean_summary_dir, clean_comment_cut_dir, matrix_similarity_dir):
    # 加载comment
    # 读取整个csv文件
    import pandas as pd
    csv_data = pd.read_csv("ML_model_1_res.csv")

    res_results = csv_data["similarity"]

    cur = 0

    pathDir = os.listdir(clean_summary_dir)
    resu = []
    all_P, all_R, all_F, all_F2 = 0, 0, 0, 0
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
        ppall = len(pathDir) - 1
        video_time_slice = []
        for i, n in enumerate(summary):
            video_time_slice.append(n["video"].split("-")[1])

        print(video_time_slice)

        # n个剧情简介对应M块弹幕
        similarity_list = []
        for i, n in enumerate(summary):
            flags = 0
            # video_time = n["video"].split("-")
            ps_init = 0
            s_score = []
            danmu_cut = ""

            for j, m in enumerate(danmu):

                if ps_init == m["cut"]:
                    danmu_cut += " " + m["danmaku_clean"]
                else:

                    # todo 2. 计算句子相似度
                    jjs = res_results[cur]
                    cur += 1

                    ps_init = m["cut"]
                    s_score.append(jjs)

                    danmu_cut = m["danmaku_clean"]
                    # flags += 1

            similarity_list.append(s_score)  # 4*200

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
        mas = np.array(similarity_list)
        y_pred = mas.argmax(axis=0)
        # y_pred.extend(dp_similarity.get_path(similarity_list))

        print(len(y_pred))

        # acc = metrics.precision_recall_fscore_support(y_true, y_pred)

        f1_score = metrics.f1_score(y_true, y_pred, average='weighted')
        macro_f1_score = metrics.f1_score(y_true, y_pred, average='macro')
        micro_f1_score = metrics.f1_score(y_true, y_pred, average='micro')
        macro_prf = precision_recall_fscore_support(y_true, y_pred, average='macro')
        # target_names = ['class 0', 'class 1', 'class 2']
        # score = metrics.classification_report(y_true, y_pred,target_names)
        # weighted_prf = precision_recall_fscore_support(y_true, y_pred, average='weighted')
        # target_names = ['class 0', 'class 1', 'class 2']
        # score = metrics.classification_report(y_true, y_pred,target_names)

        print(f1_score)
        print(macro_f1_score)
        print(micro_f1_score)
        # 保存相似度矩阵
        # matrix_similarity = os.path.join(matrix_similarity_dir, danmu_file)
        # save_similarity_cosine(similarity_list, matrix_similarity)
        print(danmu_file[0])

        P, R, F = macro_prf[0], macro_prf[1], macro_prf[2]
        F2 = 2 * P * R / (P + R)
        all_P += P
        all_R += R
        all_F += F
        all_F2 += F2
        # resu.append({"P": str(P), "R": str(R), "F": str(F2), "macro_F": str(F)})

    resu.append({"P": str(all_P / ppall), "R": str(all_R / ppall), "F": str(all_F2 / ppall),
                 "macro_F": str(all_F / ppall)})
    datas.append(resu)

    matrix_similarity = os.path.join(matrix_similarity_dir, "20201211ML_VAE_Cut3_classify_" + method)
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
    method = "classify3"
    # method = "bm25"

    get_similarity2(method, clean_summary_dir, clean_comment_cut_dir, matrix_similarity_dir)
