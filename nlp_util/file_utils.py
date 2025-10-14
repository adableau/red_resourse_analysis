# coding:utf-8
import json
import numpy as np
import csv


def replace_sep(fin, fout, sep_ini, sep_fin):
    """
    Replace delimiter in a file.
    """
    fin = open(fin, "r")
    fout = open(fout, "w")
    for line in fin:
        fout.write(line.replace(sep_ini, sep_fin))
    fin.close()
    fout.close()


def remove_quotes(fin, fout):
    """ Remove quotes in lines.
    If a line has odd number quotes, remove all quotes in this line.
    """
    fin = open(fin)
    fout = open(fout, "w")
    for line in fin:
        fout.write(line.replace("\"", ""))
    fin.close()
    fout.close()


def load_danmu(file_path):
    datas = []
    lines = open(file_path, 'r', encoding='utf8').read().strip().split('\n')
    for line in lines:
        data = json.loads(line)
        datas.append(data)
    return datas


def load_csv(file_path):
    datas = []
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as fr:
        cr = csv.reader(fr)
        for line in cr:
            datas.append(line)
    return datas


def read_txtfile(file_path):
    # lines = np.loadtxt(file_path, encoding='utf8',dtype=float)
    flines = open(file_path, 'r', encoding='utf-8').readlines()

    return flines


def save_similarity_cosine(similarity_list, matrix_similarity_dir):
    wr = open(matrix_similarity_dir, 'w', encoding='utf8')
    wr.write(str(similarity_list))
    wr.close()


def dump_to_json(datas, fout):
    for data in datas:
        fout.write(json.dumps(data, sort_keys=True, separators=(',', ': '), ensure_ascii=False))
        fout.write('\n')
    fout.close()


def load_from_json(fin):
    datas = []
    for line in fin:
        data = json.loads(line)
        datas.append(data)
    return datas
