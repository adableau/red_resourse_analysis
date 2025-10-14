import glob

import pandas as pd
import os

import os
import pandas as pd


def read_csv_folder(folder_path, columns):
    df_list = []
    for filename in os.listdir(folder_path):
        if filename.endswith('.csv'):
            file_path = os.path.join(folder_path, filename)
            # 假设景点名称是在第一个下划线和第二个下划线之间
            # 并且确保从列表中提取单个字符串值
            namee = os.path.basename(file_path).split('_')[1]  # 修正这里
            print(namee)
            df = pd.read_csv(file_path, header=None)  # 添加header=None假设文件没有表头
            # 检查 'ip属地_城市' 和 'ip属地_省份' 是否包含 '上海'
            if '上海' in df['ip属地_城市'].values or '上海' in df['ip属地_省份'].values:
                df_list.append(df)

            #df_list.append(df)
    return pd.concat(df_list, ignore_index=True)


# 定义文件夹路径和列名
folder1 = './'
columns1 = ['页码', '微博id', '微博作者', '发布时间', '微博内容', '转发数', '评论数', '点赞数', '发布于', 'ip属地_城市', 'ip属地_省份', 'ip属地_国家']

# 读取文件夹中的 CSV 文件
#df1 = read_csv_folder(folder1, columns1)

# 合并 DataFrame
# combined_df = pd.concat([df1, df2, df3], ignore_index=True)


# 使用glob读取所有csv文件
csv_files = glob.glob('*.csv')


import glob
import pandas as pd

# 使用glob读取所有csv文件
csv_files = glob.glob('*.csv')

# 创建一个字典来存储每个文件的记录数
file_record_counts = {}

# 遍历所有文件，读取并统计记录数
for file in csv_files:
    df = pd.read_csv(file)
    file_record_counts[file] = len(df)

print(file_record_counts)


# 读取并合并所有CSV文件
df = pd.concat([pd.read_csv(file) for file in csv_files], ignore_index=True)

# 去除重复行（基于所有列）
final_df = df.drop_duplicates(subset=df.columns[0:4])
# 可选：将结果保存为新的 CSV 文件
df.to_csv('mergedall20250214.csv', index=False, encoding='utf_8', header=None)
