import pandas as pd

# 读取CSV文件
csv_file_path = 'merged_with_categories.csv'  # 你的CSV文件路径
df = pd.read_csv(csv_file_path)

# 统计每个子类目的评论频次
subcategory_comment_counts = df.groupby('子类目')['评论数'].count().reset_index(name='评论频次')

# 计算每个子类目下的情感数目：积极、消极和中性
positive_comments = df[df['正负情感'] == '积极'].groupby('子类目')['正负情感'].count().reset_index(name='积极情感数')
neutral_comments = df[df['正负情感'] == '中性'].groupby('子类目')['正负情感'].count().reset_index(name='中性情感数')
negative_comments = df[df['正负情感'] == '消极'].groupby('子类目')['正负情感'].count().reset_index(name='消极情感数')

# 合并统计结果
result = pd.merge(subcategory_comment_counts, positive_comments[['子类目', '积极情感数']], on='子类目', how='left')
result = pd.merge(result, neutral_comments[['子类目', '中性情感数']], on='子类目', how='left')
result = pd.merge(result, negative_comments[['子类目', '消极情感数']], on='子类目', how='left')


# 需要确保所有参与计算的列都是数字类型
result['评论频次'] = pd.to_numeric(result['评论频次'], errors='coerce')  # 强制转换为数字类型
result['积极情感数'] = pd.to_numeric(result['积极情感数'], errors='coerce')
result['消极情感数'] = pd.to_numeric(result['消极情感数'], errors='coerce')
result['中性情感数'] = pd.to_numeric(result['中性情感数'], errors='coerce')

# 处理缺失值（如果需要）
df.fillna(0, inplace=True)  # 将NaN填充为0，或者选择其他处理方式
# 处理缺失值，填充为0
result = result.fillna(0)


# 筛选出积极情感的评论
positive_comments_df = df[df['正负情感'] == '消极']

# 保存积极评论为新的CSV文件
positive_comments_file_path = 'negative_comments.csv'  # 输出文件路径
positive_comments_df.to_csv(positive_comments_file_path, index=False)

print(f"积极评论已保存为 '{positive_comments_file_path}'")

# 计算积极、消极和中性情感占比
result['积极情感占比(%)'] = (result['积极情感数'] / result['评论频次']) * 100
result['消极情感占比(%)'] = (result['消极情感数'] / result['评论频次']) * 100
result['中性情感占比(%)'] = (result['中性情感数'] / result['评论频次']) * 100

# 打印统计结果
print("子类目情感统计结果：")
print(result[['子类目', '评论频次', '积极情感数', '中性情感数', '消极情感数', '积极情感占比(%)', '消极情感占比(%)', '中性情感占比(%)']])

# 保存统计结果为CSV文件
output_csv_path = 'subcategory_emotion_distribution.csv'  # 输出文件路径
result[['子类目', '评论频次', '积极情感数', '中性情感数', '消极情感数', '积极情感占比(%)', '消极情感占比(%)', '中性情感占比(%)']].to_csv(output_csv_path, index=False)

print(f"统计结果已保存为 '{output_csv_path}'")
