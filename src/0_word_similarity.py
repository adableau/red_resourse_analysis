# -*- encoding:utf-8 -*-
import os

from sklearn import metrics
from sklearn.metrics import precision_recall_fscore_support

import dp_similarity
import file_utils
import jaccard_similarity as jsm
from models import bm25_similarity_tets


def get_similarity(method, clean_summary_dir, clean_comment_cut_dir, matrix_similarity_dir):
    # 加载comment
    pathDir = os.listdir(clean_summary_dir)

    # 1. 加载词向量
    # wv_from_text = similarity.gensim_vec()
    for idx, file_name_txt in enumerate(pathDir):
        datas = []
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

        # n个剧情简介对应M块弹幕
        similarity_list = []
        for n in summary:
            # video_time = n["video"].split("-")
            ps_init = 0
            s_score = []
            danmu_cut = ""

            for m in danmu:

                if ps_init == m["cut"]:
                    danmu_cut += " " + m["danmaku_clean"]
                else:

                    # todo 2. 计算句子相似度
                    if method == "jaccard_similarity":
                        jjs = jsm.combine_jaccard_similarity(danmu_cut, n["content_clean"])
                    elif method == "bm25":
                        jjs = bm25_similarity_tets.cal_bm25_sim(danmu_cut, n["content_clean"])

                    ps_init = m["cut"]
                    s_score.append(jjs)

                    danmu_cut = m["danmaku_clean"]

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

        #          if cut_num_init == ps_init:
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

        matrix_similarity = os.path.join(matrix_similarity_dir, danmu_file[0] + "_" + method)
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
