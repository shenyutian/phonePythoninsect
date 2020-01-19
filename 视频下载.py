import you_get
import sys
import time
import threading


def downloads(url, path):
    """列表下载"""
    sys.argv = ['you-get', '--playlist', '-o', path, url]
    try:
        you_get.main()
    except:
        print("错误：" + url)


def download(url, path):
    """单独下载"""
    sys.argv = ['you-get', '-o', path, url]
    try:
        you_get.main()
    except:
        print("错误：" + url)



url = "https://www.bilibili.com/video/av19995678"
# url = "https://www.bilibili.com/video/av64784430"
path = "E:\\电影\\北风Spark 2.0从入门到精通"
# path = "D:\\电影\\厦门大学_林子雨_spark编程基础"
downloads(url, path)

