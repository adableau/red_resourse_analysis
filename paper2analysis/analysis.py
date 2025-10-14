import pandas as pd
import glob

# 使用glob读取所有csv文件
csv_files = glob.glob('*.csv')

# 读取并合并所有CSV文件
df = pd.concat([pd.read_csv(file) for file in csv_files], ignore_index=True)

# 统计子类目的频率
sub_category_counts = df['子类目'].value_counts()

# 计算子类目的百分比
sub_category_percentages = df['子类目'].value_counts(normalize=True) * 100
# 合并频率和百分比
sub_category_stats = pd.DataFrame({
    '频率': sub_category_counts,
    '百分比': sub_category_percentages
}).reset_index()

# 重命名列
sub_category_stats.columns = ['子类目', '频率', '百分比']
print(sub_category_stats)


#设施服务、旅游资源、休闲娱乐、环境与氛围、游客满意度与反馈


# 统计每个子类目的评论频次
comment_counts = df.groupby('子类目')['评论数'].sum()

# 按子类目和情感（正负情感）分类，统计每种情感的评论数量
positive_counts = df[df['正负情感'] == 1].groupby('子类目')['评论数'].sum()
negative_counts = df[df['正负情感'] == -1].groupby('子类目')['评论数'].sum()

# 合并统计结果
emotion_stats = pd.DataFrame({
    '评论频次': comment_counts,
    '积极评论数': positive_counts,
    '消极评论数': negative_counts
}).fillna(0)

# 计算积极和消极情感的百分比
emotion_stats['积极情感百分比'] = (emotion_stats['积极评论数'] / emotion_stats['评论频次']) * 100
emotion_stats['消极情感百分比'] = (emotion_stats['消极评论数'] / emotion_stats['评论频次']) * 100
# 输出结果
print(emotion_stats[['评论频次', '积极情感百分比', '消极情感百分比']])
