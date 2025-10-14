# -*- coding: utf-8 -*-

# from src.Segmentation import Segmentation
from Segmentation import Segmentation
import os
import math
import csv

class Rough(object):
    def __init__(self, seg):
        self.seg = seg

    def score_1(self, prediction, target):
        pre_list = self.seg.cut(prediction)
        tar_list = self.seg.cut(target)
        denominator = len(tar_list)
        numerator = 0.01
        for w in tar_list:
            if w in pre_list:
                numerator += 1
        return numerator / denominator

    def score_2(self, prediction, target):
        pre_list = self.seg.cut(prediction)
        tar_list = self.seg.cut(target)

        pl_2 = []
        for i in range(len(pre_list)):
            if i < len(pre_list) - 2:
                pl_2.append(pre_list[i] + pre_list[i + 1])

        tl_2 = []
        for i in range(len(tar_list)):
            if i < len(tar_list) - 2:
                tl_2.append(tar_list[i] + tar_list[i + 1])

        denominator = len(tl_2)
        numerator = 0.01
        for w in tl_2:
            if w in pl_2:
                numerator += 1
        return numerator / denominator


def resTocsv(gold_dir_path, pred_dir_path):
    goldDir = os.listdir(gold_dir_path)
    predDir = os.listdir(pred_dir_path)
    for (idx, goldPath), (idx, predPath) in zip(enumerate(goldDir), enumerate(predDir)):
        print(idx)
    # for idx, goldPath in enumerate(goldDir):
    # for goldPath, predPath in zip(goldDir, predDir):

        # predPath = os.path.join(pred_dir_path, goldPath[1][0], '.txt')
        goldPath = os.path.join(gold_dir_path, goldPath)
        predPath = os.path.join(pred_dir_path, predPath)
        gold_abstract = []
        pred_abstract = []

        with open(goldPath, 'r') as fr1, open(predPath, 'r') as fr2:
            for line in fr1.readlines():
                gold = line[line.rindex('###'):].strip()
                gold_abstract.append(gold)

            flag = False
            for line in fr2.readlines():
                if flag == True:
                    pred = line[line.index('\t') + 1:].strip()
                    pred_abstract.append(pred)
                    flag = False
                if '关键句子：' in line:
                    flag = True

        seg = Segmentation()
        rough = Rough(seg)
        score1 = []
        score2 = []
        # if len(gold_abstract) != len(pred_abstract):
        #     print("Length error!!!")

        for i in range(min(len(pred_abstract), len(gold_abstract))):
            score1.append(rough.score_1(pred_abstract[i], gold_abstract[i]))
            score2.append(rough.score_2(pred_abstract[i], gold_abstract[i]))
        avg1 = float(sum(score1)/len(score1))
        avg2 = float(sum(score2)/len(score2))

        csv_path1 = "../result/evaluate/rough1/"
        csv_name = os.path.join(csv_path1, str(idx) + '.csv')
        with open(csv_name, "w", newline="") as datacsv:
            csvwriter = csv.writer(datacsv, dialect=("excel"))
            for j in range(len(score1)):
                csvwriter.writerow([j, score1[j]])
            csvwriter.writerow(['avg', avg1])

        csv_path2 = "../result/evaluate/rough2/"
        csv_name = os.path.join(csv_path2, str(idx)+'.csv')
        with open(csv_name, "w", newline="") as datacsv:
            csvwriter = csv.writer(datacsv, dialect=("excel"))
            for j in range(len(score2)):
                csvwriter.writerow([j, score2[j]])
            csvwriter.writerow(['avg', avg2])


if __name__ == '__main__':
    gold_dir = "../data/gold/"
    pred_dir = "../result/comment/"

    resTocsv(gold_dir, pred_dir)

    # gold_abstract = []
    # pred_abstract = []
    # with open(gold_path, 'r') as fr1, open(pred_path, 'r') as fr2:
    #     for line in fr1.readlines():
    #         gold = line[line.rindex('###'):].strip()
    #         gold_abstract.append(gold)
    #
    #     flag = False
    #     for line in fr2.readlines():
    #         if flag == True:
    #             pred = line[line.index('\t')+1:].strip()
    #             pred_abstract.append(pred)
    #             flag = False
    #         if '关键句子：' in line:
    #             flag = True
    #
    # seg = Segmentation()
    # rough = Rough(seg)
    # score1 = []
    # score2 = []
    # if len(gold_abstract) != len(pred_abstract):
    #     print("Length error!!!")
    #
    # for i in range(len(pred_abstract)):
    #     score1.append(rough.score_1(pred_abstract[i], gold_abstract[i]))
    #     score2.append(rough.score_2(pred_abstract[i], gold_abstract[i]))
    #
    # print(score1)
    # print(score2)
    # print(float(sum(score1)/len(score1)))
    # print(float(sum(score2)/len(score2)))












