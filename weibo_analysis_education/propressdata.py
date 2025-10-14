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
            df['景点'] = namee  # 现在namee是一个字符串
            df_list.append(df)
    return pd.concat(df_list, ignore_index=True)


# 定义文件夹路径和列名
folder1 = './'
columns1 = ['页码', '微博id', '微博作者', '发布时间', '微博内容', '转发数', '评论数', '点赞数', '发布于', 'ip属地_城市', 'ip属地_省份', 'ip属地_国家']

# 读取文件夹中的 CSV 文件
df1 = read_csv_folder(folder1, columns1)

# 合并 DataFrame
# combined_df = pd.concat([df1, df2, df3], ignore_index=True)

# 去除重复行（基于所有列）
final_df = df1.drop_duplicates(subset=df1.columns[2:5])

# 可选：将结果保存为新的 CSV 文件
final_df.to_csv('1education_combined_weibo_data.csv', index=False, encoding='utf_8', header=None)
