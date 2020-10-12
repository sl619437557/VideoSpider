#通过request获取HTML，将关键词检索得到的视频链接存入mongoDB，需要指定关键词和爬取页，尚未完善异常处理
#数据库字段示范：
# {
#     "href": "www.bilibili.com/video/BV1aC4y1W7fD",
#     "keywords": "马拉松",
#     "title": "如果你1公里跑不进5分，就别总想着马拉松跑进3个半小时"
# }

import requests
from bs4 import BeautifulSoup
import re
import pymongo
import sys

def BiliSpider(keywords,page):
  url = "https://search.bilibili.com/all?keyword="+keywords+"&page="+str(page)
  client = pymongo.MongoClient(host='127.0.0.1')
  payload = {}
  headers = {
    'Cookie': 'main_confirmation=C/Mb1jdk4KPIlFgveREEr4jMzGMI2VRMQJz7MIvUIoc='
  }
  response = requests.request("GET", url, headers=headers, data = payload)
  #将获取的html代码存入mongoDB
  htmldic={"ketwords":keywords,"page":page,"html":response.text}
  db=client.BiliBili
  htmlcollections=db.htmlpage
  result=htmlcollections.update_one(htmldic,{'$set':htmldic},upsert=True)

  soup = BeautifulSoup(response.text, 'html.parser')
  item = soup.find_all(class_='video-item matrix')
  #当爬取不到视频时结束
  if not item:
    print("爬取结束")
    sys.exit()
  for i in item:
    i=str(i).replace(' ','')
    #正则匹配视频标题
    title=re.findall("title.*?>",i)
    title=re.findall("\".*?\"",str(title))[0][1:-1]
    #视频链接
    href=re.findall("class=\"title\".*?>",i)
    href=re.findall("//.*?\"",str(href))[0][2:-13]
    #观看
    #UP主
    # 以上tag暂不添加需求
    video={"keywords":keywords,"title":title,"href":href}
    videocollections=db.videoes
    result=videocollections.update_one(video,{'$set':video},upsert=True)
  print("B站"+keywords+'第'+str(page)+'页爬取结束')