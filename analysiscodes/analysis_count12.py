# -*- coding: utf-8 -*-
import pandas as pd
import networkx as nx
import itertools
from collections import defaultdict

# 读取数据

import pandas as pd
from datetime import datetime

# 重新定义之前的函数，以便于重新执行代码状态
from data_utils import save_datas
import pandas as pd
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei']  #设置中文字体
plt.rcParams['axes.unicode_minus'] = False
# 加载CSV文件
# 假设CSV文件路径已正确设置
#file_path = "lycombined_weibo_data.cs"
file_path = "3redsourse_combined_weibo_data.csv"
import pandas as pd

# 加载 CSV 文件
df = pd.read_csv(file_path)


# 如果你还想同时满足省份或国家也是特定值，可以进一步筛选
# 例如，筛选出省份是上海和国家是中国的数据,发布于,ip属地_城市,ip属地_省份
shanghai_data = df[(df['ip属地_城市'] == '上海') |(df['发布于'] == '上海') | (df['ip属地_省份'] == '上海')]

# 查看筛选后的数据
print(shanghai_data)

# 保存筛选后的数据到新的 CSV 文件
shanghai_data.to_csv('shanghai_data.csv', index=False)
