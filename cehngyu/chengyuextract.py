import requests
import jieba.posseg as pseg

def get_idioms_from_api():
    response = requests.get("https://api.sampleapis.com/idioms/idioms")  # 示例API
    if response.status_code == 200:
        return [idiom['phrase'] for idiom in response.json()]
    else:
        return []

idioms_list = get_idioms_from_api()

def extract_idioms_and_nouns(text):
    idioms = [word for word in idioms_list if word in text]
    words = pseg.cut(text)
    nouns = [word for word, flag in words if flag.startswith('n')]
    return idioms, nouns

text = "学海无涯苦作舟，天道酬勤，每个人都在为自己的目标努力奋斗。"
idioms, nouns = extract_idioms_and_nouns(text)
print("成语:", idioms)
print("名词:", nouns)
