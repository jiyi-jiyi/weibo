import requests
import json
import os
import time, random
import pandas
from datetime import date, datetime, timedelta
from bs4 import BeautifulSoup

def standardize_date(created_at):
    """标准化微博发布时间"""
    if "刚刚" in created_at:
        ts = datetime.now()
    elif "分钟" in created_at:
        minute = created_at[: created_at.find("分钟")]
        minute = timedelta(minutes=int(minute))
        ts = datetime.now() - minute
    elif "小时" in created_at:
        hour = created_at[: created_at.find("小时")]
        hour = timedelta(hours=int(hour))
        ts = datetime.now() - hour
    elif "昨天" in created_at:
        day = timedelta(days=1)
        ts = datetime.now() - day
    else:
        created_at = created_at.replace("+0800 ", "")
        ts = datetime.strptime(created_at, "%c")

    full_created_at = ts.strftime("%Y-%m-%d %H:%M:%S")
    return full_created_at

def remove_html_tag(text):
    soup = BeautifulSoup(text, "html.parser")
    return soup.get_text(separator="\n")

data = {"time":[], "text":[], "url":[]}
cookie_string = 'SCF=Al8bIfcBanK02294JsMGRoQP-oQymZ0z70FBREp42tMSCzpWRBdByu457zkDfvhCs3pSVEDw0wRUyzp2DciBO-0.; SUB=_2A25F1hl2DeRhGeFM7VcU8i3NyDuIHXVmqhS-rDV6PUJbktAYLWT3kW1NQNYm7ZixBC5I4vyYtOBfldR4IFEbrb-T; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WW0Xqy_dUA0V1hKwy_I_sqY5JpX5KMhUgL.FoMESo-feoepe0M2dJLoIE.LxK-LB--L1h2LxKBLBonLB.2LxKML12-L1h.LxKMLBKzL12-Reo20S5tt; SSOLoginState=1758619942; ALF=1761211942; MLOGIN=1; _T_WM=28901705560; WEIBOCN_FROM=1110006030; XSRF-TOKEN=e4c741; mweibo_short_token=d5b431316f; M_WEIBOCN_PARAMS=luicode%3D10000011%26lfid%3D2304132691175262_-_WEIBO_SECOND_PROFILE_WEIBO%26fid%3D1005052691175262%26uicode%3D10000011'
cookies = {}
for pair in cookie_string.split(';'):
    key, value = pair.split('=', 1)
    cookies[key.strip()] = value.strip()

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'mweibo-pwa': '1',
    'priority': 'u=1, i',
    'referer': 'https://m.weibo.cn/',
    'sec-ch-ua': '"Not;A=Brand";v="99", "Microsoft Edge";v="139", "Chromium";v="139"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36 Edg/139.0.0.0',
}

pic_headers = {
    'accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'priority': 'i',
    'referer': 'https://m.weibo.cn/',
    'sec-ch-ua': '"Not;A=Brand";v="99", "Microsoft Edge";v="139", "Chromium";v="139"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'image',
    'sec-fetch-mode': 'no-cors',
    'sec-fetch-site': 'cross-site',
    'sec-fetch-storage-access': 'active',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36 Edg/139.0.0.0',
}

s = requests.Session()
s.cookies.update(cookies)
name = '折木一茶'
path = './' + name
if not os.path.exists(path):
    os.makedirs(path)

url = 'https://m.weibo.cn/api/container/getIndex?'
params = {
    'containerid': '100103type=1&q=' + name,
    'page_type': 'searchall'
}
response = s.get(url=url, params=params, headers=headers)
user_id = json.loads(response.text)["data"]["cards"][0]["card_group"][0]["user"]["id"]

url = 'https://m.weibo.cn/api/container/getIndex?'
params = {
        'luicode': '10000011',
        'lfid': '230413' + str(user_id) + '_-_WEIBO_SECOND_PROFILE_WEIBO',
        'type': 'uid',
        'value': user_id,
        'containerid': '107603' + str(user_id),
}
res = s.get(url=url, params=params, headers=headers)
res = json.loads(res.text)

while True:

    for card in res["data"]["cards"]:
        info = card["mblog"]
        retweeted_status = info.get("retweeted_status")
        if retweeted_status and retweeted_status.get("id"):
            data['text'].append(remove_html_tag(card["mblog"]["text"]) + '\n原微博：\n' + remove_html_tag(info["retweeted_status"]["text"]))
        else:
            data['text'].append(remove_html_tag(card["mblog"]["text"]))
        data['time'].append(standardize_date(card["mblog"]["created_at"]))
        data['url'].append("https://m.weibo.cn/detail/" + info["id"])

    print(res["data"]["cardlistInfo"]["since_id"])
    params = {
        'luicode': '10000011',
        'lfid': '230413' + str(user_id) + '_-_WEIBO_SECOND_PROFILE_WEIBO',
        'type': 'uid',
        'value': user_id,
        'containerid': '107603' + str(user_id),
        'since_id': res["data"]["cardlistInfo"]["since_id"],
    }
    time.sleep(random.uniform(2, 5))
    res = s.get(url=url, params=params, headers=headers)
    if res.status_code != 200:
        print(res.text)
        break
    res = json.loads(res.text)
    if res["ok"] != 1:
        print(res)
        break
    
df = pandas.DataFrame(data)
df.to_excel('zmyc.xlsx')