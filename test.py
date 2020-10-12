from BiliBiliSpider import BiliSpider
import time
from CNTVSpider import CNTVSpider
if __name__=='__main__':
    keyword='马拉松'
    pages=20
    for page in range(1,pages+1):
        CNTVSpider(keyword,page)
        time.sleep(5)