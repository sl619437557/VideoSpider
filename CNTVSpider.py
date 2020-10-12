#央视网视频爬取，直接获取json存入MongoDB，暂无异常处理需求
#数据库文档示范
# {
#     "TV": "其他",
#     "all_title": "[马拉松]非洲选手包揽上海马拉松男女冠军",
#     "channel": "体育",
#     "durations": 0,
#     "id": "22737320",
#     "imglink": "https://p1.img.cctvpic.com/fmspic/2012/12/03/4ddbf81169374c4394c4d6ed5c11d70d-180.jpg",
#     "playtime": {
#         "$numberLong": "1354490897000"
#     },
#     "title": "[<font color=\"red\">马拉松</font>]非洲选手包揽上海<font color=\"red\">马拉松</font>男女冠军",
#     "uploadtime": "2012-12-03 07:28:17",
#     "urllink": "http://sports.cntv.cn/20121203/100822.shtml"
#  }

import requests
import pymongo
import sys
def CNTVSpider(keywords,page):
    url = "https://search.cctv.com/ifsearch.php?page="+str(page)+"&qtext="+keywords+"&sort=relevance&type=video"
    payload = {}
    headers= {}
    response = requests.request("GET", url, headers=headers, data = payload)
    request_json=response.json()
    videolist=request_json['list']
    if not videolist:
        print("爬取异常")
        sys.exit()
    client = pymongo.MongoClient(host='127.0.0.1')
    db=client.CNTV
    videocollection=db.videoes
    for i in videolist:
        result=videocollection.update_one(i,{'$set':i},upsert=True)
    print("央视网"+keywords+"第"+str(page)+"页"+"爬取结束")