#!/home/fy/.virtualenvs/spider_py2/bin/python2.7
# coding=utf-8
import urllib2
import cookielib


def mk_cookie():
    cookiejar = cookielib.CookieJar()
    handler = urllib2.HTTPCookieProcessor(cookiejar)
    url = "https://www.lagou.com/jobs/list_" + 'java' + "?city=%E5%85%A8%E5%9B%BD"
    # url="https://www.lagou.com/jobs/positionAjax.json"

    opener = urllib2.build_opener(handler)
    opener.addheaders = [
        ("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36")]
    opener.open(url)

    cookieStr = ""
    for item in cookiejar:
        cookieStr = cookieStr + item.name + "=" + item.value + ";"
    return cookieStr
