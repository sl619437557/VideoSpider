import you_get
import sys
import pymongo
import re

#从数据库查询相应关键词数据导出下载链接文档
def getCNTVfile(keyword):
    client = pymongo.MongoClient(host='127.0.0.1')
    db=client.CNTV
    collection=db.videoes
    result=collection.find({'all_title':re.compile(keyword)})
    filename='CNTV_URL.txt'
    with open(filename,"a") as file_object:
        for i in result:
            file_object.write(i['urllink']+'\n')

def getBiliBilifile(keyword):
    client = pymongo.MongoClient(host='127.0.0.1')
    db=client.BiliBili
    collection=db.videoes
    result=collection.find({'title':re.compile(keyword)})
    filename='BiliBili_URL.txt'
    with open(filename,"a") as file_object:
        for i in result:
            file_object.write(i['href']+'\n')

#根据链接下载视频文件到指定文件夹，通过platform指定平台
#2020.10.10 添加异常捕捉
def Download(platform):
    filename = platform+'_URL.txt'
    outputfile='DOWNLOADED_URL.txt'
    with open(filename,'r') as file_object:
        lines=file_object.readlines()
    while lines:
        line=lines.pop(0)
        with open(filename,'w') as file_object2:
            for i in lines:
                file_object2.write(i)
        with open(outputfile,'a') as f:
            f.write(line)
        try:
            url=line.strip()
            path=r'C:\Users\sunl1\PycharmProjects\VideoSpider\video'
            sys.argv=['you-get','-o',path,url]
            #-i查询
            you_get.main()
        except BaseException:
            with open('ERROR_LOG.txt','a') as file_object:
                    file_object.write(url+"\n")

# getCNTVfile("跑")
getBiliBilifile("跑")
# Download('CNTV')
