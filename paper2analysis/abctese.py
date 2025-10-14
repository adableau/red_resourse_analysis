import pandas as pd
import requests
import json

# 调用大模型进行情感分析、子类目标注和总类别分类
def analyze_content(content):
    url = "http://114.115.247.223:7965/api_sse/v1/stream-chat"
    headers = {
        "Content-Type": "application/json",
        "Accept": "text/event-stream"
    }
    data = {
        "model": "deepseek-r1",
        "messages": [
            {"role": "user", "content": f"请分析以下内容的输出为情感（正向、中立、负向）、子类目和总类别（文化、旅游、历史、景点、教育、建筑、政治），以：分割：{content}"}
        ]
    }

    full_response = ""
    with requests.post(url, headers=headers, data=json.dumps(data), stream=True) as response:
        if response.status_code == 200:
            for line in response.iter_lines():
                if line:
                    decoded_line = line.decode('utf-8')
                    if decoded_line.startswith("data:"):
                        json_data = json.loads(decoded_line[5:].strip())
                        reasoning_content = json_data["Choices"][0]["Delta"]["ReasoningContent"]
                        full_response += reasoning_content
        else:
            print(f"请求失败，状态码: {response.status_code}")
            return None, None, None

    # 解析大模型的响应
    try:
        # 假设大模型的响应格式为：情感：正向，子类目：景点介绍，总类别：旅游
        parts = full_response.split("，")
        sentiment = parts[0].split("：")[1].strip()
        sub_category = parts[1].split("：")[1].strip()
        main_category = parts[2].split("：")[1].strip()
        return sentiment, sub_category, main_category
    except Exception as e:
        print(f"解析大模型响应失败: {e}")
        return None, None, None

# 读取CSV文件并处理
def process_csv(input_file, output_file):
    # 读取CSV文件
    df = pd.read_csv(input_file)

    # 初始化新列
    df["情感"] = ""
    df["子类目"] = ""
    df["总类别"] = ""

    # 逐行处理微博内容
    for index, row in df.iterrows():
        content = row["微博内容"]
        print(f"正在处理第 {index + 1} 条微博内容: {content}")
        sentiment, sub_category, main_category = analyze_content(content)
        df.at[index, "情感"] = sentiment
        df.at[index, "子类目"] = sub_category
        df.at[index, "总类别"] = main_category

    # 保存到新的CSV文件
    df.to_csv(output_file, index=False, encoding="utf_8")
    print(f"处理完成，结果已保存到 {output_file}")

# 主程序
if __name__ == "__main__":
    input_file = "web.csv"  # 输入CSV文件路径
    output_file = "outputweibo.csv"  # 输出CSV文件路径
    process_csv(input_file, output_file)
