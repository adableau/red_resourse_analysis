#encoding=gbk
import pandas as pd
import networkx as nx
import itertools
from collections import defaultdict



# 读取数据

import pandas as pd
from datetime import datetime

# 重新定义之前的函数，以便于重新执行代码状态
from data_utils import save_datas


def convert_to_wos_format(df):
    wos_data = []
#微博id,微博作者,发布时间,微博内容,转发数,评论数,点赞数,发布于,ip属地_城市,ip属地_省份,ip属地_国家
    for _, row in df.iterrows():
        title = row['微博内容'][:50]  # 使用内容的前50个字符作为标题
        author = row['微博作者']
        year = row['发布时间']
        abstract = row['微博内容']
        # 这里省略了关键词提取步骤

        # 构造 WOS 记录
        wos_record = f'PT J\nAU {author}\nPY {year}\nTI {title}\nAB {abstract}\nER\n\n'
        wos_data.append(wos_record)

    return wos_data

# 假设这里有一个示例 DataFrame，我们将用上述函数转换它（此部分为示例，实际使用时应替换为真实数据加载代码）
# 示例 DataFrame 创建（为了代码执行，这里使用示例数据）
#df_example = pd.DataFrame({
    #    '微博内容': ['这是一个微博内容示例。', '另一个微博内容示例。'],
    #'微博作者': ['作者A', '作者B'],
    #'发布时间': [pd.Timestamp('2023-01-01'), pd.Timestamp('2024-01-01')]
#})
df_example = pd.read_csv('download_weibo_data.csv')
# 转换示例 DataFrame 为 WOS 格式
wos_data_example = convert_to_wos_format(df_example)

# 将 WOS 数据转换为文本并打印（实际应用中应保存到文件）
wos_text_example = ''.join(wos_data_example)
print(wos_text_example)

save_datas(wos_text_example, 'wos_text_example.txt', trans_to_str=False)
