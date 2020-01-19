import pymysql
import urllib.request
import re

sqlName = "111.229.170.213"


def get_data_forsqlurl():
    """"获取所有数据"""
    """数据库base表中取得参数路径"""
    conn = pymysql.connect(sqlName, "root", "123456", "cellphone")
    # 获取mysql游标
    cursor = conn.cursor()
    # 从test_url 表中将id 和 url取出来
    sql = "select uid, url from testurl where uid < 1478254 ORDER BY uid DESC limit 0,4000"
    cursor.execute(sql)
    datas = cursor.fetchall()
    cursor.close()
    conn.close()
    return datas


def get_img_list(url):
    """爬取网站，获取正确的图片集"""
    html = urllib.request.urlopen(url).read()
    html = html.decode("gbk")
    html = str(html)
    # 无轮播图处理
    if html.find('nav end') != -1:
        html = html.split('nav end')
        html = html[1]
        html = html.split("SPU")
        html = html[0]
        regex = "title=\"(.*?)\" class.*?swiper-lazy.*?//(.*?.jpg).*?>"
    else:
        print("无轮播图：" + url)
        html = html.split('item-pic')
        html = html[1]
        html = html.split("点击看更多图片")
        html = html[0]
        regex = ">()<a.*?//(.*?.jpg).*?>"

    # 匹配正则式
    datas = re.findall(regex, html)
    # for data in datas:
        # print(data)
    return datas


def set_img_sql_list():
    """增加相机信息数据  listdatas 数据集"""
    conn = pymysql.connect(sqlName, "root", "123456", "cellphone")
    # 获取mysql游标
    cursor = conn.cursor()

    sql = "insert into phone_photo" \
          " " \
          "values (null , %s, %s, %s, %s);"
    try:
        # 2阶 sql语句
        cursor.executemany(sql, listdatas)
        # 元组列表插入sql
        # cursor.execute(sql, listdatas)
        conn.commit()
    except Exception as e:
        # 回滚数据
        conn.rollback()
        print("失败：" + sql)
    cursor.close()
    conn.close()
    return 1


def replace_sub(str):
    """正则式替换图片中的_axb"""
    p = "_(.*?)/"
    # print(re.compile(p).findall(str))
    str = re.sub(p, "/", str)
    return str


datas = get_data_forsqlurl()
# 二阶列表，存放需要的数据集
listdatas = []
for data in datas:
    config_id = data[0]
    # 拼接得到真正的链接
    url = ''.join(data[1])
    # 处理url
    url = url.replace("http://detail.zol.com.cn", "https://wap.zol.com.cn").replace("param.shtml", "index.html")
    print(url)
    tuple_datas = get_img_list(url)
    for tuple_data in tuple_datas:
        img = tuple_data[1]
        img = replace_sub(img)
        list_data = list(tuple_data)
        # 第一个元素插入
        list_data.insert(0, config_id)
        # 最后一个元素插入
        list_data.append(img)
        # print(list_data)
        listdatas.append(tuple(list_data))
set_img_sql_list()

# url = "https://wap.zol.com.cn/1270/1269219/index.html"
# get_img_list(url)
