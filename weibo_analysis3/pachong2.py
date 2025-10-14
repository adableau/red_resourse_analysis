import os
import re
import requests
import pandas as pd
import datetime
import time

# 请求头，模拟浏览器访问
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.110 Safari/537.36",
    "accept": "application/json, text/plain, */*",
}


def trans_time(v_str):
    """转换GMT时间为标准格式"""
    GMT_FORMAT = '%a %b %d %H:%M:%S +0800 %Y'
    timeArray = datetime.datetime.strptime(v_str, GMT_FORMAT)
    return timeArray.strftime("%Y-%m-%d %H:%M:%S")


def getLongText(v_id):
    """获取长微博内容"""
    url = f'https://m.weibo.cn/statuses/extend?id={v_id}'

    for _ in range(3):  # 允许最多重试 3 次
        try:
            r = requests.get(url, headers=headers, timeout=10)
            if r.status_code == 200:
                json_data = r.json()
                long_text = json_data['data'].get('longTextContent', '')
                return re.sub(r'<[^>]+>', '', long_text)  # 清除 HTML 标签
            else:
                print(f"获取长微博失败，状态码: {r.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"请求错误: {e}")
        time.sleep(2)  # 避免短时间连续请求
    return ""


def get_user_weibo_list(user_id, max_pages=10):
    """爬取某个用户的所有微博"""
    base_url = "https://m.weibo.cn/api/container/getIndex"

    # 获取用户 containerid
    params = {
        "type": "uid",
        "value": user_id
    }

    try:
        r = requests.get(base_url, headers=headers, params=params, timeout=10)
        r.raise_for_status()  # 如果请求失败，抛出异常
        json_data = r.json()
    except requests.exceptions.RequestException as e:
        print(f"请求失败: {e}")
        return []
    except requests.exceptions.JSONDecodeError:
        print("JSON 解析失败，可能是 API 返回了空数据")
        return []

    try:
        containerid = json_data["data"]["tabsInfo"]["tabs"][1]["containerid"]
    except (KeyError, IndexError):
        print("无法解析用户的微博 containerid，可能是用户隐私设置问题")
        return []

    all_weibo = []
    page = 1

    while page <= max_pages:
        print(f"=== 正在爬取用户 {user_id} 的第 {page} 页微博 ===")
        params = {
            "containerid": containerid,
            "page": page
        }

        try:
            r = requests.get(base_url, headers=headers, params=params, timeout=10)
            if r.status_code != 200:
                print(f"请求失败，状态码: {r.status_code}")
                break

            json_data = r.json()
            cards = json_data.get("data", {}).get("cards", [])
            if not cards:
                print("没有更多微博了")
                break
        except requests.exceptions.RequestException as e:
            print(f"请求失败: {e}")
            break
        except requests.exceptions.JSONDecodeError:
            print("JSON 解析失败，可能是 API 返回了空数据")
            break

        for card in cards:
            if "mblog" not in card:
                continue
            mblog = card["mblog"]

            # 提取微博信息
            weibo_id = mblog["id"]
            text = re.sub(r'<[^>]+>', '', mblog["text"])  # 清除 HTML 标签
            created_at = trans_time(mblog["created_at"])
            author = mblog["user"]["screen_name"]
            reposts_count = mblog.get("reposts_count", 0)
            comments_count = mblog.get("comments_count", 0)
            attitudes_count = mblog.get("attitudes_count", 0)
            is_long_text = mblog.get("isLongText", False)

            if is_long_text:
                text = getLongText(weibo_id)

            all_weibo.append([
                weibo_id, author, created_at, text,
                reposts_count, comments_count, attitudes_count
            ])

        page += 1
        time.sleep(2)  # 避免触发反爬机制

    return all_weibo


def save_to_csv(user_id, data):
    """保存数据到 CSV"""
    if not data:
        print("无数据可保存")
        return

    df = pd.DataFrame(data, columns=["微博id", "微博作者", "发布时间", "微博内容", "转发数", "评论数", "点赞数"])
    file_name = f"微博用户_{user_id}.csv"

    if os.path.exists(file_name):
        df.to_csv(file_name, mode="a", header=False, index=False, encoding="utf_8_sig")
    else:
        df.to_csv(file_name, index=False, encoding="utf_8_sig")

    print(f"数据已保存到 {file_name}")


if __name__ == '__main__':
    user_id = "2803301701"  # 需要爬取的微博用户 ID（示例为人民日报）
    max_pages = 50  # 爬取的最大页数
    weibo_data = get_user_weibo_list(user_id, max_pages)
    save_to_csv(user_id, weibo_data)
