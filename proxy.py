#!/home/fy/.virtualenvs/spider_py2/bin/python2.7
# coding=utf-8
import requests


# 获取代理和删除代理
def get_proxy():
    return requests.get("http://127.0.0.1:5010/get/").text


def delete_proxy(proxy):
    requests.get("http://127.0.0.1:5010/delete/?proxy={}".format(proxy))
