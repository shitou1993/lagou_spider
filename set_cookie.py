#!/home/fy/.virtualenvs/spider_py2/bin/python2.7
# coding=utf-8
from selenium import webdriver
import time


driver=webdriver.PhantomJS()
time.sleep(5)
driver.get("https://www.lagou.com/jobs/list_" + 'java' + "?city=%E5%85%A8%E5%9B%BD")
for cookie in driver.get_cookies():
    print "%s -> %s" % (cookie['name'], cookie['value'])
