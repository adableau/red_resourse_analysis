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


if __name__ == '__main__':
    model_name = "deepseek-r1"
    user_message = "你是谁"
    messages = [{"role": "user", "content": user_message}]

    print(f"发送消息: {user_message}")
    print("接收到的回复:")

    full_response = ""  # 用于存储完整的回复

    for chunk in stream_chat(model_name, messages):
        try:
            # 尝试将 chunk 解析为 JSON
            json_data = json.loads(chunk)
            # 根据 JSON 结构提取文本内容
            if "Choices" in json_data and len(json_data["Choices"]) > 0 and "Delta" in json_data["Choices"][0] and "ReasoningContent" in json_data["Choices"][0]["Delta"]:
                text = json_data["Choices"][0]["Delta"]["ReasoningContent"]
                print(text, end="", flush=True)  # 实时打印，不换行
                full_response += text  # 将文本添加到完整回复中
            elif "Choices" in json_data and len(json_data["Choices"]) > 0 and "finish_reason" in json_data["Choices"][0]:
                finish_reason = json_data["Choices"][0]["finish_reason"]
                print(f"\n完成原因: {finish_reason}")
            else:
                print(f"无法解析的 JSON 数据: {chunk}")

        except json.JSONDecodeError:
            print(f"非 JSON 数据: {chunk}") # 如果不是JSON，直接打印
        except Exception as e:
            print(f"处理数据时发生错误: {e}")

    print("\n对话结束")
    print(f"完整回复: {full_response}")  # 打印完整的回复
