import matplotlib.pyplot as plt
import numpy as np

# 数据
categories = ['没有', '活动', '展览', '看到', '生活', '打卡', '还有', '喜欢', '开放', '好吃']
verbs = [181, 147, 140, 115, 110, 107, 105, 104, 88, 82]
nouns = [2899, 1565, 1291, 738, 717, 416, 367, 288, 265, 229]
adjectives = [82, 82, 82, 82, 82, 82, 82, 82, 82, 82]
idioms = [27, 11, 7, 6, 6, 6, 3, 3, 3, 3]
four_char_phrases = [203, 83, 62, 53, 39, 36, 32, 27, 0, 0]

# 设置角度
angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False).tolist()

# 为了使图形闭合，重复第一个值
categories += categories[:1]
angles += angles[:1]

# 创建子图
fig, ax = plt.subplots(figsize=(8, 8), dpi=80, subplot_kw=dict(polar=True))

# 绘制每个组的条形图
ax.bar(angles, verbs + [verbs[0]], width=0.3, color='red', alpha=0.6, label='动词')
ax.bar(angles, nouns + [nouns[0]], width=0.3, color='blue', alpha=0.6, label='名词')
ax.bar(angles, adjectives + [adjectives[0]], width=0.3, color='green', alpha=0.6, label='形容词')
ax.bar(angles, idioms + [idioms[0]], width=0.3, color='purple', alpha=0.6, label='成语')
ax.bar(angles, four_char_phrases + [four_char_phrases[0]], width=0.3, color='orange', alpha=0.6, label='四字词语')

# 设置标签
ax.set_yticklabels([])
ax.set_xticks(angles[:-1])
ax.set_xticklabels(categories, rotation=45, ha='right')

# 添加标题
ax.set_title('各类别词语频次的径向条形图', size=16, color='black', y=1.1)

# 添加图例
ax.legend(loc='upper right', bbox_to_anchor=(1.1, 1.1))

# 显示图形
plt.tight_layout()
plt.show()
