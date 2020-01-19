import _thread
import threading

import pymysql
import urllib.request
import re

sqlName = "111.229.170.213"


def get_data_forsqlurl(start, end):
    """数据库base表中取得image路径"""
    conn = pymysql.connect(sqlName, "root", "123456", "cellphone")
    # 获取mysql游标
    cursor = conn.cursor()
    sql = "select base_id, base_remarks from phone_base"
    sql = sql + " limit " + str(start) + ", " + str(end)
    print(sql)
    cursor.execute(sql)
    datas = cursor.fetchall()
    cursor.close()
    conn.close()
    return datas


def geturl_data(url):
    """获取到的所有数据网站的url"""
    html = urllib.request.urlopen(url).read()
    html = html.decode("gbk")
    html = str(html)
    """裁切 从下面的文字开始"""
    html = html.split("综述介绍")
    html = html[1]
    html = html.split("参数")
    html = html[0]
    if len(html) > 115:
        html = html.split("图片")
        html = html[1]
    html = html.replace(" ", "")
    print(html)
    regex = "<ahref=\"(.*?)\"target="
    regex = re.compile(regex)
    url = re.findall(regex, html)
    # print("url\t", url)
    return "http://detail.zol.com.cn" + ''.join(url)


def get_data(url):
    """获取到全部数据的网站，用来获取参数列表"""
    html = urllib.request.urlopen(url).read()
    html = html.decode("gbk")
    html = str(html)
    html = html.split('>外观</td>')
    html = html[1]
    html = html.split("功能与服务")
    html = html[0]
    html = re.sub("<a.*?/a>", "", html)
    html = re.sub("<i.*?/a>", "", html)
    # 对空格回车动手
    html = html.replace("\r", "")
    html = html.replace("\n", "")
    # html = html.replace(" ", "")
    html = html.replace("<br />", "+")
    html = html.replace("<br/>", "+")
    # html = html.replace("<p>", "")
    # html = html.replace("</p>", "")
    # 干掉空格
    html = html.replace("&nbsp;", "")
    regex = "<span id=\"newPmVal_([0-9]{1,2})\">(.*?)</span>"
    # 匹配正则式
    datas = re.findall(regex, html)
    # 创建list 列表
    listdata = []
    # 参数长度
    length = len(datas)
    # 根据参数长度来判断 添加内容 6去掉空格 4,5不变 3修改
    if length == 6:
        del datas[4]
        for data in datas:
            listdata.append(data[1])
    elif length == 3:
        if datas[2][1] == '':
            for data in datas:
                listdata.append(data[1])
            listdata.insert(1, '')
            listdata.insert(1, '')
        else:
            for data in datas:
                listdata.append(data[1])
    elif length < 2:
        listdata.append(datas[0][1])
    else:
        for data in datas:
            listdata.append(data[1])
    # 长度不够，加空格来凑5个元素
    while len(listdata) < 5:
        listdata.append("")
    print(listdata)
    return listdata


def set_facade_mysql(facade_id, listdata):
    """增加数据  facade_id外观id  listdata 数据"""
    listdata.append(facade_id)
    listdata = tuple(listdata[1:])
    print("listdata:\t", listdata)
    conn = pymysql.connect(sqlName, "root", "123456", "cellphone")
    # 获取mysql游标
    cursor = conn.cursor()
    sql = "insert into phone_facade" \
          "(facade_id, facade_size, facade_weight, facade_texture, facade_other) " \
          "values (%s, %s, %s, %s, %s);"
    try:
        #  2阶 sql语句
        # cursor.executemany(sql, listdata)
        #
        cursor.execute(sql, listdata)
        conn.commit()
    except Exception as e:
        # 回滚数据
        conn.rollback()
        print("失败：" + sql)
    cursor.close()
    conn.close()
    return 1


def set_testsql(uid, url):
    listdata = []
    listdata.append(uid)
    listdata.append(url)
    conn = pymysql.connect(sqlName, "root", "123456", "cellphone")
    # 获取mysql游标
    cursor = conn.cursor()
    sql = "insert into testurl" \
          "(uid, url) " \
          "values (%s, %s);"
    try:
        #  2阶 sql语句
        # cursor.executemany(sql, listdata)
        # 元组列表插入sql
        cursor.execute(sql, listdata)
        conn.commit()
        print("成功")
    except Exception as e:
        # 回滚数据
        conn.rollback()
        print("失败：" + str(uid))
    cursor.close()
    conn.close()
    return 1


class myThread(threading.Thread):
    """新的线程来处理"""
    def __init__(self, starts, end):
        threading.Thread.__init__(self)
        self.starts = starts
        self.end = end

    def run(self):
        """ url = "http://detail.zol.com.cn/1282/1281307/param.shtml" """
        datas = get_data_forsqlurl(self.starts, self.end)
        for data in datas:
            facade_id = data[0]
            url = ''.join(data[1])
            # 每台设备参数网址的获取
            url = "http://detail.zol.com.cn" + url
            url = geturl_data(url)
            print("uid\t", facade_id)
            print("参数详情url：", url)
            set_testsql(facade_id, url)


# """主线程 安排5个线程来进行数据获取"""
# thread1 = myThread(0, 500)
# thread2 = myThread(500, 1000)
# thread3 = myThread(1000, 1500)
# thread4 = myThread(1500, 2000)
# thread5 = myThread(2000, 2500)
# thread1.start()
# thread2.start()
# thread3.start()
# thread4.start()
# thread5.start()





"""之前的方法"""
""" url = "http://detail.zol.com.cn/1282/1281307/param.shtml" """
datas = get_data_forsqlurl(1528, 200)
for data in datas:
    facade_id = data[0]
    url = ''.join(data[1])
    # 每台设备参数网址的获取
    url = "http://detail.zol.com.cn" + url
    url = geturl_data(url)
    print("uid\t", facade_id)
    print("参数详情url：", url)
    set_testsql(facade_id, url)
# 参数详情
# listdata = get_data(url)
# set_facade_mysql(facade_id, listdata)
