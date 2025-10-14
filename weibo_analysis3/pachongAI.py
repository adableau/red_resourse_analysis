import os
import re  # 正则表达式提取文本
from jsonpath import jsonpath  # 解析json数据
import requests  # 发送请求
import pandas as pd  # 存取csv文件
import datetime  # 转换时间用

# 请求头
headers = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Mobile Safari/537.36",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "accept-encoding": "gzip, deflate, br",
}

# 超时时间
TIMEOUT = 5


def trans_time(v_str):
    """转换GMT时间为标准格式"""
    try:
        GMT_FORMAT = '%a %b %d %H:%M:%S +0800 %Y'
        timeArray = datetime.datetime.strptime(v_str, GMT_FORMAT)
        return timeArray.strftime("%Y-%m-%d %H:%M:%S")
    except Exception as e:
        print(f"时间格式转换失败: {v_str}, 错误: {e}")
        return v_str


def getLongText(v_id):
    """爬取长微博全文"""
    url = f'https://m.weibo.cn/statuses/extend?id={v_id}'
    try:
        r = requests.get(url, headers=headers, timeout=TIMEOUT)
        json_data = r.json()
        long_text = json_data.get('data', {}).get('longTextContent', "")
        return re.sub(r'<[^>]+>', '', long_text)  # 正则去HTML标签
    except Exception as e:
        print(f"获取长微博失败: {e}")
        return ""


def get_weibo_list(v_keyword, v_max_page):
    """爬取微博内容列表"""
    for page in range(1, v_max_page + 1):
        print(f'=== 开始爬取第 {page} 页微博 ===')

        url = 'https://m.weibo.cn/api/container/getIndex'
        params = {"containerid": f"100103type=1&q={v_keyword}", "page_type": "searchall", "page": page}

        try:
            r = requests.get(url, headers=headers, params=params, timeout=TIMEOUT)
            if r.status_code != 200:
                print(f"请求失败, 状态码: {r.status_code}")
                continue

            cards = r.json().get("data", {}).get("cards", [])
            if not cards:
                print("未找到微博数据，跳过")
                continue

            # 解析字段
            id_list = jsonpath(cards, '$..mblog.id') or []
            author_list = jsonpath(cards, '$..mblog.user.screen_name') or []
            time_list = jsonpath(cards, '$..mblog.created_at') or []
            text_list = jsonpath(cards, '$..mblog.text') or []
            reposts_count_list = jsonpath(cards, '$..mblog.reposts_count') or []
            comments_count_list = jsonpath(cards, '$..mblog.comments_count') or []
            attitudes_count_list = jsonpath(cards, '$..mblog.attitudes_count') or []
            isLongText_list = jsonpath(cards, '$..mblog.isLongText') or []
            region_name_list = jsonpath(cards, '$..mblog.region_name') or []
            status_city_list = jsonpath(cards, '$..mblog.status_city') or []
            status_province_list = jsonpath(cards, '$..mblog.status_province') or []
            status_country_list = jsonpath(cards, '$..mblog.status_country') or []

            # 数据清洗: 去除 HTML 标签
            text2_list = [re.sub(r'<[^>]+>', '', text) for text in text_list]

            # 处理长文本微博
            for idx, is_long in enumerate(isLongText_list):
                if is_long and idx < len(id_list):
                    text2_list[idx] = getLongText(id_list[idx])

            # 统一列表长度
            min_length = min(len(id_list), len(author_list), len(time_list), len(text2_list),
                             len(reposts_count_list), len(comments_count_list), len(attitudes_count_list),
                             len(region_name_list), len(status_city_list), len(status_province_list), len(status_country_list))

            id_list = id_list[:min_length]
            author_list = author_list[:min_length]
            time_list = time_list[:min_length]
            text2_list = text2_list[:min_length]
            reposts_count_list = reposts_count_list[:min_length]
            comments_count_list = comments_count_list[:min_length]
            attitudes_count_list = attitudes_count_list[:min_length]
            region_name_list = region_name_list[:min_length]
            status_city_list = status_city_list[:min_length]
            status_province_list = status_province_list[:min_length]
            status_country_list = status_country_list[:min_length]

            # 构建 DataFrame
            df = pd.DataFrame({
                '页码': [page] * min_length,
                '微博id': id_list,
                '微博作者': author_list,
                '发布时间': time_list,
                '微博内容': text2_list,
                '转发数': reposts_count_list,
                '评论数': comments_count_list,
                '点赞数': attitudes_count_list,
                '发布于': region_name_list,
                'ip属地_城市': status_city_list,
                'ip属地_省份': status_province_list,
                'ip属地_国家': status_country_list,
            })

            # 保存文件
            if os.path.exists(v_weibo_file):
                header = None
            else:
                header = df.columns.tolist()

            df.to_csv(v_weibo_file, mode='a+', index=False, header=header, encoding='utf_8_sig')
            print(f'csv 保存成功: {v_weibo_file}')

        except Exception as e:
            print(f"爬取第 {page} 页失败: {e}")


if __name__ == '__main__':
    max_search_page = 50  # 爬取前50页
    search_keyword = '高中减负'  # 关键词
    v_weibo_file = f'微博清单_{search_keyword}_前{max_search_page}页.csv'

    # 删除旧文件
    if os.path.exists(v_weibo_file):
        os.remove(v_weibo_file)
        print(f'微博清单存在，已删除: {v_weibo_file}')

    # 调用爬取微博函数
    get_weibo_list(v_keyword=search_keyword, v_max_page=max_search_page)

    # 数据清洗: 去重
    try:
        df = pd.read_csv(v_weibo_file)
        df.drop_duplicates(subset=['微博id'], inplace=True, keep='first')
        df.to_csv(v_weibo_file, index=False, encoding='utf_8_sig')
        print('数据清洗完成')
    except Exception as e:
        print(f"数据清洗失败: {e}")
