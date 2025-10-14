import glob

import pandas as pd

# 读取TXT文件，假设每行格式为 "子类目 总类别"（用制表符或空格分隔）
txt_file_path = 'leibie2'
category_dict = {}

# 读取TXT并构建子类目到总类别的映射字典
with open(txt_file_path, 'r', encoding='utf-8') as f:
    for line in f:
        parts = line.strip().split(',')  # 如果是制表符分隔的话，使用 line.split('\t') 也行
        if len(parts) == 2:
            main_category = parts[0]
            sub_categories = parts[1].split(',')  # 子类别由逗号分隔
            for sub_category in sub_categories:
                category_dict[sub_category.strip()] = main_category

# 读取CSV文件



# 使用glob读取所有csv文件
csv_files = glob.glob('*.csv')

# 读取并合并所有CSV文件
df = pd.concat([pd.read_csv(file) for file in csv_files], ignore_index=True)



# 根据子类目添加总类别
df['总类别'] = df['子类目'].map(category_dict).fillna('未知类别')

# 保存新的CSV文件
output_csv_path = 'merged_with_categories.csv'
df.to_csv(output_csv_path, index=False)

print(f"文件已保存为 '{output_csv_path}'")
