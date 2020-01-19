import pymysql
import urllib.request
import re


def get_data_forsqlurl():
    """数据库base表中取得image路径"""
    conn = pymysql.connect("localhost", "root", "123456", "cellphone")
    # 获取mysql游标
    cursor = conn.cursor()
    sql = "select base_remarks from phone_base"
    cursor.execute(sql)
    datas = cursor.fetchall()
    cursor.close()
    conn.close()
    return datas


def geturl_data(url):
    """获取到全部数据的网站"""
    html = urllib.request.urlopen(url).read()
    html = html.decode("gbk")
    html = str(html)
    """裁切 从下面的文字开始"""
    html = html.split("nav__list clearfix")
    html = html[1]
    html = html.split("_j_top_promotion")
    html = html[0]
    html = html.split("图片")
    html = html[1]
    html = html.split("参数")
    html = html[0]
    html = html.replace(" ", "")
    regex = "<ahref=\"(.*?)\"target="
    regex = re.compile(regex)
    url = re.findall(regex, html)
    return "http://detail.zol.com.cn" + ''.join(url)


def get_data(url):
    """获取到全部数据的网站"""
    html = urllib.request.urlopen(url).read()
    html = html.decode("gbk")
    html = str(html)
    html = html.split("name=\"s-5\">外观</td>")
    html = html[1]
    html = html.split("name=\"s-6\">功能与服务</td>")
    html = html[0]
    html = re.sub("<a.*?/a>", "", html)
    # 对空格回车动手
    html = html.replace("\r", "")
    html = html.replace("\n", "")
    # html = html.replace(" ", "")
    html = html.replace("<br />", "+")
    # html = html.replace("<p>", "")
    # html = html.replace("</p>", "")
    html = html.replace("&nbsp;", "")
    regex = "<span id=\"newPmVal_([0-9]{1,2})\">(.*?)</span>"
    datas = re.findall(regex, html)
    del datas[4]
    for data in datas:
        print(data)


""" 
datas = get_data_forsqlurl()
for url in datas:
    url = ''.join(url)
    url = "http://detail.zol.com.cn" + url
    url = geturl_data(url)
"""
url = "http://detail.zol.com.cn/1282/1281307/param.shtml"
get_data(url)
