import numpy as np
import gensim
import torch
import time
import json
from src.prepocessor import load_from_json

# 数据集格式化加载。。。
import argparse

parser = argparse.ArgumentParser(description='train.py')
parser.add_argument('-n_emb', type=int, default=512, help="Embedding size")
parser.add_argument('-batch_size', type=int, default=64, help="Batch size")
parser.add_argument('-vocab_size', type=int, default=20000, help="Vocabulary size")
parser.add_argument('-epoch', type=int, default=50, help="Number of epoch")
parser.add_argument('-report', type=int, default=500, help="Number of report interval")
parser.add_argument('-lr', type=float, default=3e-4, help="Learning rate")
parser.add_argument('-restore', type=str, default='', help="Restoring model path")
parser.add_argument('-mode', type=str, default='train', help="Train or test")
parser.add_argument('-dir', type=str, default='ckpt', help="Checkpoint directory")
parser.add_argument('-max_len', type=int, default=20, help="Limited length for text")
parser.add_argument('-n_img', type=int, default=5, help="Number of input images")
parser.add_argument('-n_com', type=int, default=5, help="Number of input comments")

opt = parser.parse_args()

data_path = ''
train_path, test_path, dev_path = data_path + 'train-context.json', data_path + 'test-candidate.json', data_path + 'dev-candidate.json'
vocab_path = data_path + 'Tencent_AILab_ChineseEmbedding.txt'

vocabs = json.load(open(vocab_path, 'r', encoding='utf8'))['word2id']
rev_vocabs = json.load(open(vocab_path, 'r', encoding='utf8'))['id2word']
opt.vocab_size = len(vocabs)


class DataSet(torch.utils.data.Dataset):
    def __init__(self, data_path, vocabs, is_train=True, imgs=None):
        print("starting load...")
        print(data_path)
        start_time = time.time()
        self.datas = load_from_json(open(data_path, 'r', encoding='utf8'))
        print("loading time:", time.time() - start_time)

        self.vocabs = vocabs
        self.vocab_size = len(self.vocabs)
        self.is_train = is_train

    def __len__(self):
        return len(self.datas)

    # 映射函数get 方法
    def __getitem__(self, index):
        data = self.datas[index]
        cut_slice, playtime = data['cut'], data['playtime']




        # 加载comments

    def load_comments(self, context):
        max_len = 20
        n_com = 5
        return DataSet.padding(context, max_len * n_com)

    @staticmethod
    def padding(data, max_len):
        data = data.split()
        if len(data) > max_len - 2:
            data = data[:max_len - 2]
        Y = list(map(lambda t: vocabs.get(t, 3), data))
        Y = [1] + Y + [2]
        length = len(Y)
        Y = torch.cat([torch.LongTensor(Y), torch.zeros(max_len - length).long()])
        return Y


def load_embedding(path):
    embedding_index = {}
    f = open(path, encoding='utf8')
    for index, line in enumerate(f):
        if index == 0:
            continue
        values = line.split(' ')
        word = values[0]
        coefs = np.asarray(values[1:], dtype='float32')
        embedding_index[word] = coefs
    f.close()
    return embedding_index


# load_embedding('Tencent_AILab_ChineseEmbedding.txt')

wv_from_text = gensim.models.KeyedVectors.load_word2vec_format('Tencent_AILab_ChineseEmbedding.txt', binary=False)
wv_from_text.init_sims(replace=True)  # 神奇，很省内存，可以运算most_similar



