import pandas as pd
import os

import pandas as pd
import os

filename = './微博清单_中共一大会址_前100页.csv'
filename = './微博清单_中共二大会址_前80页.csv'
filename = './微博清单_四行仓库_前100页.csv'
filename = './微博清单_鲁迅墓_前80页.csv'
filename = './微博清单_鲁迅小道_前100页.csv'
filename = './微博清单_鲁迅故居_前80页.csv'
filename = './微博清单_海关大楼_前40页.csv'
filename = './微博清单_龙华革命烈士_前100页.csv'
filename = './微博清单_宋庆龄故居_前100页.csv'
filename = './微博清单_上海鲁迅纪念馆_前80页.csv'
filename = './微博清单_巴金旧居_前40页.csv'
filename = './微博清单_郭沫若旧居_前80页.csv'
filename = './微博清单_中央政治局机关_前40页.csv'
# 指定读取文件时的编码，如果你确定默认编码能正常工作，这行可以省略
df = pd.read_csv(filename, header=None, encoding='utf-8')

# 去除重复行（基于所有列）
final_df = df.drop_duplicates(subset=df.columns[2:5])

# 构建新文件名和路径
new_filename = 'new_' + os.path.basename(filename)
new_filepath = os.path.join(os.path.dirname(filename), new_filename)

# 可选：将结果保存为新的 CSV 文件
final_df.to_csv(new_filepath, index=False, encoding='utf_8_sig', header=None)
