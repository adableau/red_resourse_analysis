import pandas as pd
from snownlp import SnowNLP


def analyze_sentiment(text):
    """分析文本情感，返回情感倾向得分"""
    return SnowNLP(text).sentiments


def sentiment_polarity(score):
    """根据情感得分返回情感极性"""

    return 1 if score >= 0.6 else 0


def main():
    # 加载CSV文件
    file_path = "1redsourse_combined_weibo_data.csv"  # 请确保这里的路径与你的文件匹配
    df = pd.read_csv(file_path)

    # 确保微博内容列的名称与你的CSV文件中的列名匹配
    if '微博内容' in df.columns:
        # 对每条微博内容应用情感分析函数，并将结果作为新列添加到DataFrame中
        df['情感得分'] = df['微博内容'].apply(analyze_sentiment)

        # 应用情感极性判断逻辑
        df['情感极性'] = df['情感得分'].apply(sentiment_polarity)

        # 保存到新的CSV文件中
        output_file_path = "2analyzed_2024031combined_weibo_data.csv"  # 指定输出文件的路径
        df.to_csv(output_file_path, index=False)
        print("分析完成，结果已保存至:", output_file_path)
    else:
        print("错误：DataFrame中没有找到'微博内容'列。")


if __name__ == '__main__':
    main()
