import pandas as pd
import requests
import json

def stream_chat(model, messages):
    """
    调用 SSE 接口进行流式对话。

    Args:
        model (str): 模型名称。
        messages (list): 对话消息列表，每个消息是一个字典，包含 "role" 和 "content"。

    Yields:
        str: 从 SSE 流中接收到的数据块。
    """

    url = "http://114.115.247.223:7965/api_sse/v1/stream-chat"
    headers = {
        "Content-Type": "application/json",
        "Accept": "text/event-stream"  # 关键：指定接受 SSE 数据流
    }
    data = {
        "model": model,
        "messages": messages
    }

    try:
        with requests.post(url, headers=headers, json=data, stream=True) as response:
            response.raise_for_status()  # 检查 HTTP 状态码

            for line in response.iter_lines():
                # 过滤掉空行和注释行
                if line:
                    decoded_line = line.decode('utf-8')
                    if decoded_line.startswith("data:"):
                        # 提取 data 部分
                        data_content = decoded_line[5:].strip()
                        yield data_content
                    elif decoded_line.startswith(":ping"):
                        # 处理 ping 事件 (可选)
                        print("Received ping from server.")
                    else:
                        print(f"Received unexpected line: {decoded_line}")


    except requests.exceptions.RequestException as e:
        print(f"请求出错: {e}")
    except Exception as e:
        print(f"发生错误: {e}")


def analyze_weibo(weibo_content, model_name):
    """
    使用大模型分析微博内容的情感、子类目和总类别。

    Args:
        weibo_content (str): 微博内容。
        model_name (str): 大模型名称。

    Returns:
        tuple: (情感, 子类目, 总类别)
    """

    prompt = f"""请分析以下微博内容的情感倾向（正向、中立、负向），子类目（描述微博内容的主题），以及总类别（文化、旅游、历史、景点、教育、建筑、政治）。
    微博内容：{weibo_content}
    请以JSON格式返回结果，格式如下：
    {{
        "情感": "...",
        "子类目": "...",
        "总类别": "..."
    }}
    """

    messages = [{"role": "user", "content": prompt}]
    full_response = ""

    for chunk in stream_chat(model_name, messages):
        try:
            json_data = json.loads(chunk)
            if "Choices" in json_data and len(json_data["Choices"]) > 0 and "Delta" in json_data["Choices"][0] and "ReasoningContent" in json_data["Choices"][0]["Delta"]:
                text = json_data["Choices"][0]["Delta"]["ReasoningContent"]
                full_response += text
            elif "Choices" in json_data and len(json_data["Choices"]) > 0 and "finish_reason" in json_data["Choices"][0]:
                pass # 忽略完成原因
            else:
                print(f"无法解析的 JSON 数据: {chunk}")

        except json.JSONDecodeError:
            print(f"非 JSON 数据: {chunk}")
        except Exception as e:
            print(f"处理数据时发生错误: {e}")

    try:
        # 尝试解析完整的回复
        analysis_result = json.loads(full_response)
        emotion = analysis_result.get("情感", "未知")
        subcategory = analysis_result.get("子类目", "未知")
        category = analysis_result.get("总类别", "未知")
        return emotion, subcategory, category
    except json.JSONDecodeError:
        print(f"无法解析完整回复: {full_response}")
        return "未知", "未知", "未知"
    except Exception as e:
        print(f"分析结果时发生错误: {e}")
        return "未知", "未知", "未知"


if __name__ == '__main__':
    csv_file = "web.csv"  # 替换为你的 CSV 文件名
    output_csv_file = "analyzed_weibo_data.csv"
    model_name = "deepseek-r1"

    try:
        df = pd.read_csv(csv_file, encoding='utf-8')  # 尝试 UTF-8 编码
    except UnicodeDecodeError:
        df = pd.read_csv(csv_file, encoding='gbk')  # 如果 UTF-8 失败，尝试 GBK 编码
    except Exception as e:
        print(f"读取 CSV 文件时发生错误: {e}")
        exit()

    # 创建新的列
    df["情感"] = ""
    df["子类目"] = ""
    df["总类别"] = ""

    for index, row in df.iterrows():
        weibo_content = str(row["微博内容"])  # 确保微博内容是字符串
        print(f"正在分析微博: {weibo_content[:50]}...")  # 打印前 50 个字符

        emotion, subcategory, category = analyze_weibo(weibo_content, model_name)

        df.loc[index, "情感"] = emotion
        df.loc[index, "子类目"] = subcategory
        df.loc[index, "总类别"] = category

        print(f"情感: {emotion}, 子类目: {subcategory}, 总类别: {category}")

    try:
        df.to_csv(output_csv_file, encoding='utf-8-sig', index=False)  # 使用 utf-8-sig 编码
        print(f"分析结果已保存到: {output_csv_file}")
    except Exception as e:
        print(f"保存 CSV 文件时发生错误: {e}")
