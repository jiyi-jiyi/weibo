import requests
import json
import os
import time, random

cookies = {
    'SCF': 'Al8bIfcBanK02294JsMGRoQP-oQymZ0z70FBREp42tMS8Dj9x1GHxL9seM0bgWPs2gkjfm0TJ3hlARuAFT4TBUo.',
    'SUB': '_2A25FqdIFDeRhGeFM7VcU8i3NyDuIHXVmx2vNrDV6PUJbktAYLWfwkW1NQNYm7W1QRIj4XZQm-Bndzg9vntkxaH5y',
    'SUBP': '0033WrSXqPxfM725Ws9jqgMF55529P9D9WW0Xqy_dUA0V1hKwy_I_sqY5NHD95QNeoqfSKz0eKeNWs4DqcjDi--fi-88iKnpi--Xi-zRi-iWi--NiKy8iKn4i--Ni-2EiKy81hzpe0Bt',
    'SSOLoginState': '1756209749',
    'ALF': '1758801749',
    '_T_WM': '24506474145',
    'MLOGIN': '1',
    'WEIBOCN_FROM': '1110106030',
    'XSRF-TOKEN': '125a5c',
    'mweibo_short_token': '6982c21306',
    'M_WEIBOCN_PARAMS': 'oid%3D3925543424937094%26luicode%3D10000011%26lfid%3D231583%26fid%3D100103type%253D1%2526q%253D%25E5%259B%25B0%25E6%25AD%25BB%25E4%25B8%25AA%25E6%2588%2591%26uicode%3D10000011',
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


name = '困死个我'
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