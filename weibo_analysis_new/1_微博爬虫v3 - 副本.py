# 程序功能: 按关键字爬取微博清单
# 程序作者: 马哥python说
import os
import re  # 正则表达式提取文本
from jsonpath import parse  # 解析json数据
import requests  # 发送请求
import pandas as pd  # 存取csv文件
import datetime  # 转换时间用
import time  # 添加延时
import json  # 用于打印json数据

# 请求头
headers = {
	"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
	"accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
	"accept-encoding": "gzip, deflate, br",
}


def trans_time(v_str):
	"""转换GMT时间为标准格式"""
	GMT_FORMAT = '%a %b %d %H:%M:%S +0800 %Y'
	timeArray = datetime.datetime.strptime(v_str, GMT_FORMAT)
	ret_time = timeArray.strftime("%Y-%m-%d %H:%M:%S")
	return ret_time


def getLongText(v_id):
	"""爬取长微博全文"""
	url = 'https://m.weibo.cn/statuses/extend?id=' + str(v_id)
	r = requests.get(url, headers=headers)
	json_data = r.json()
	long_text = json_data['data']['longTextContent']
	# 微博内容-正则表达式数据清洗
	dr = re.compile(r'<[^>]+>', re.S)
	long_text2 = dr.sub('', long_text)
	# print(long_text2)
	return long_text2


def get_weibo_list(v_keyword, v_max_page):
	"""
	爬取微博内容列表
	:param v_keyword: 搜索关键字
	:param v_max_page: 爬取前几页
	:return: None
	"""
	for page in range(1, v_max_page + 1):  # 从第1页开始
		print('===开始爬取第{}页微博==='.format(page))
		# 请求地址
		url = 'https://m.weibo.cn/api/container/getIndex'
		# 请求参数
		params = {
			"containerid": "100103type=1&q={}".format(v_keyword),
			"page_type": "searchall",
			"page": page
		}
		try:
			# 发送请求
			r = requests.get(url, headers=headers, params=params)
			print(f'状态码: {r.status_code}')
			
			# 打印返回的json数据，方便调试
			print('返回数据:', json.dumps(r.json(), ensure_ascii=False, indent=2)[:500] + '...')
			
			# 解析json数据
			data = r.json()
			if 'data' not in data or 'cards' not in data['data']:
				print(f'页面{page}未获取到数据，跳过')
				continue
				
			cards = data["data"]["cards"]
			print(f'获取到{len(cards)}条卡片数据')
			
			region_name_list = []
			status_city_list = []
			status_province_list = []
			status_country_list = []
			for card in cards:
				# 发布于
				try:
					region_name = card['card_group'][0]['mblog']['region_name']
					region_name_list.append(region_name)
				except:
					region_name_list.append('')
				# ip属地_城市
				try:
					status_city = card['card_group'][0]['mblog']['status_city']
					status_city_list.append(status_city)
				except:
					status_city_list.append('')
				# ip属地_省份
				try:
					status_province = card['card_group'][0]['mblog']['status_province']
					status_province_list.append(status_province)
				except:
					status_province_list.append('')
				#ip属地_国家
				try:
					status_country = card['card_group'][0]['mblog']['status_country']
					status_country_list.append(status_country)
				except:
					status_country_list.append('')
			# 使用jsonpath-ng提取数据
			jsonpath_expr = parse('$..mblog.text')
			text_list = [match.value for match in jsonpath_expr.find(cards)]
			
			# 微博内容-正则表达式数据清洗
			dr = re.compile(r'<[^>]+>', re.S)
			text2_list = []
			print('text_list is:')
			if not text_list:  # 如果未获取到微博内容，进入下一轮循环
				continue
			if type(text_list) == list and len(text_list) > 0:
				for text in text_list:
					text2 = dr.sub('', text)  # 正则表达式提取微博内容
					text2_list.append(text2)
				
			# 使用jsonpath-ng提取其他数据
			time_expr = parse('$..mblog.created_at')
			time_list = [match.value for match in time_expr.find(cards)]
			time_list = [trans_time(v_str=i) for i in time_list]
			
			author_expr = parse('$..mblog.user.screen_name')
			author_list = [match.value for match in author_expr.find(cards)]
			
			id_expr = parse('$..mblog.id')
			id_list = [match.value for match in id_expr.find(cards)]
			
			isLongText_expr = parse('$..mblog.isLongText')
			isLongText_list = [match.value for match in isLongText_expr.find(cards)]
			
			idx = 0
			for i in isLongText_list:
				if i == True:
					long_text = getLongText(v_id=id_list[idx])
					text2_list[idx] = long_text
				idx += 1
				
			# 提取统计数据
			reposts_expr = parse('$..mblog.reposts_count')
			reposts_count_list = [match.value for match in reposts_expr.find(cards)]
			
			comments_expr = parse('$..mblog.comments_count')
			comments_count_list = [match.value for match in comments_expr.find(cards)]
			
			attitudes_expr = parse('$..mblog.attitudes_count')
			attitudes_count_list = [match.value for match in attitudes_expr.find(cards)]
			# 把列表数据保存成DataFrame数据
			print('id_list:',len(id_list))
			print(len(time_list))
			print('region_name_list:',len(region_name_list))
			print(len(status_city_list))
			print(len(status_province_list))
			print(len(status_country_list))

			df = pd.DataFrame(
				{
					'页码': [page] * len(id_list),
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
				}
			)
			# 表头
			if os.path.exists(v_weibo_file):
				header = None
			else:
				header = ['页码', '微博id', '微博作者', '发布时间', '微博内容', '转发数', '评论数', '点赞数', '发布于','ip属地_城市','ip属地_省份','ip属地_国家']  # csv文件头
			# 保存到csv文件
			df.to_csv(v_weibo_file, mode='a+', index=False, header=header, encoding='utf_8_sig')
			print('csv保存成功:{}'.format(v_weibo_file))
			
		except Exception as e:
			print(f'爬取第{page}页时发生错误: {str(e)}')
			continue
			
		# 每次请求后添加随机延时，避免被反爬
		time.sleep(5)


if __name__ == '__main__':
	# 爬取前几页
	max_search_page = 50  # 爬前n页
	# 爬取关键字列表
	search_keyword = '高中双休'
	# 保存文件名
	v_weibo_file = '微博清单_{}_前{}页.csv'.format(search_keyword, max_search_page)
	# 如果csv文件存在，先删除之
	if os.path.exists(v_weibo_file):
		os.remove(v_weibo_file)
		print('微博清单存在，已删除: {}'.format(v_weibo_file))
	# 调用爬取微博函数
	get_weibo_list(v_keyword=search_keyword, v_max_page=max_search_page)
	# 数据清洗-去重
	df = pd.read_csv(v_weibo_file)
	# 删除重复数据
	df.drop_duplicates(subset=['微博id'], inplace=True, keep='first')
	# 再次保存csv文件
	df.to_csv(v_weibo_file, index=False, encoding='utf_8_sig')
	print('数据清洗完成')
