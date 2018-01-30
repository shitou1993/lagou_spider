#!/home/fy/.virtualenvs/spider_py2/bin/python2.7
# coding=utf-8
import urllib2
from bs4 import BeautifulSoup
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


# 获取每种类目的总页数
def get_num(category):
    url = "https://www.lagou.com/jobs/list_" + category + "?city=%E5%85%A8%E5%9B%BD"
    print url
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
    }
    request = urllib2.Request(url, headers=headers)
    response = urllib2.urlopen(request)
    html = response.read()
    selector = BeautifulSoup(html, 'lxml')
    text = selector.select(
        'div.page-number > span.totalNum')[0]
    return int(text.get_text().encode('utf8'))
