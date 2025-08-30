import requests
import json
import os
import time, random

cookies = {
}


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


name = ''
path = './' + name
if not os.path.exists(path):
    os.makedirs(path)

page = 0

url = 'https://m.weibo.cn/api/container/getIndex?'
params = {
    'containerid': '100103type=1&q=' + name,
    'page_type': 'searchall'
}
response = requests.get(url=url, params=params, cookies=cookies)
user_id = json.loads(response.text)["data"]["cards"][0]["card_group"][0]["user"]["id"]

url = 'https://m.weibo.cn/api/container/getSecond?'

while True:
    params = {
        'containerid': '107803' + str(user_id) + '_-_photoall',
        'page': str(page),
        'count': '24',
        'title': '图片墙',
        'luicode': '10000011',
        'lfid': '107803' + str(user_id),
    }

    response = requests.get(url=url, headers=headers, params=params, cookies=cookies)
    print(response.status_code)
    if response.status_code == 200:
        print(page)
        result = json.loads(response.text)
        if result['ok'] == 1:
            print("test")
            cards = result['data']['cards']
            for card in cards:
                for pic in card['pics']:
                    if 'video' in pic.keys():
                        temp = requests.get(url=pic['video'], headers=pic_headers)
                        with open(path+'/'+pic['mblog']['pic_ids'][0]+'.mp4','wb') as f:
                            for chunk in temp.iter_content(chunk_size=10240):
                                f.write(chunk)
                    else:
                        print(pic["mblog"]["pic_infos"][pic['mblog']["pic_ids"][0]]["original"]["url"])
                        temp = requests.get(url=pic["mblog"]["pic_infos"][pic['mblog']["pic_ids"][0]]["original"]["url"], headers=pic_headers)
                        with open(path+'/'+ pic['mblog']["id"] + '_' + pic['mblog']['pic_ids'][0]+'.jpg','wb') as f:
                            f.write(temp.content)
                    
                    time.sleep(random.uniform(0.2, 0.5))

    page+=1
