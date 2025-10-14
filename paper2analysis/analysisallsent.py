import pandas as pd

# 读取CSV文件
csv_file_path = 'merged_with_categories.csv'  # 你的CSV文件路径
df = pd.read_csv(csv_file_path)

# 统计子类目的出现次数和百分比
sub_category_counts = df['子类目'].value_counts()
sub_category_percentages = (sub_category_counts / len(df)) * 100

# 统计总类别的出现次数和百分比
total_category_counts = df['总类别'].value_counts()
total_category_percentages = (total_category_counts / len(df)) * 100

# 合并统计结果
sub_category_stats = pd.DataFrame({
    '子类目出现次数': sub_category_counts,
    '子类目百分比': sub_category_percentages
}).reset_index()
sub_category_stats.columns = ['子类目', '出现次数', '百分比']

total_category_stats = pd.DataFrame({
    '总类别出现次数': total_category_counts,
    '总类别百分比': total_category_percentages
}).reset_index()
total_category_stats.columns = ['总类别', '出现次数', '百分比']

# 打印统计结果
print("子类目统计结果：")
print(sub_category_stats)

print("\n总类别统计结果：")
print(total_category_stats)

# 保存统计结果到CSV文件
sub_category_stats.to_csv('sub_category_stats.csv', index=False)
total_category_stats.to_csv('total_category_stats.csv', index=False)

print("统计结果已保存为 'sub_category_stats.csv' 和 'total_category_stats.csv'")

# 按照总类别和子类目进行分组，并统计出现次数
category_group = df.groupby(['总类别', '子类目']).size().reset_index(name='出现次数')

# 计算每个子类目在总类别中的百分比
category_group['百分比'] = category_group.groupby('总类别')['出现次数'].transform(lambda x: (x / x.sum()) * 100)

# 打印统计结果
print("总类别与子类目联合统计结果：")
print(category_group)

# 保存统计结果为CSV文件
category_group.to_csv('category_and_subcategory_stats.csv', index=False)

print("统计结果已保存为 'category_and_subcategory_stats.csv'")
