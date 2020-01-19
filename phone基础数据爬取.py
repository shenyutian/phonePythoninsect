import pymysql
import urllib.request
import re

def get_phone_datas(url):
    """获取基础信息数据"""
    html = urllib.request.urlopen(url).read()
    html = html.decode("gbk")
    html = str(html)
    """裁切 从下面的文字开始"""
    html = html.split("title=\"产品评分由高到低\"")
    html = html[1]
    html = html.split("<h3>手机品牌报价大全</h3>")
    html = html[0]
    # 对空格回车动手
    html = html.replace("\r", "")
    html = html.replace("\t", "")
    html = html.replace("\n", "")
    html = html.replace(" ", "")
    html = html.replace("<br/>", "")
    html = html.replace("<p>", "")
    html = html.replace("</p>", "")
    regex = "<imgwidth=\"220\"height=\"165\".src=\"(.*?)\"alt=\"(.*?)\"></a>"\
            "<h3><ahref=\"(.*?)\"title=.*?<span>(.*?)</span></a></h3>.*?"\
            "</b><b.*?class=\"price-type\">(\d*?)</b></span><divclass=\"goods-promotion\">" \
            "</div>"
    regex = re.compile(regex)
    datas = re.findall(regex, html)
    # 定义一个所有数据 列表
    listdata = []
    for data in datas:
        # 取出id 号码一列
        num = str(data[2])
        # 取出 真正的id号码
        num = re.sub("\\D", "", num)
        # 定义一个列表放 当前行数据
        listnum = data + tuple(num.split())
        print(listnum)
        listdata.append(listnum)
    return listdata


def set_phone_mysql(datas):
    """增加数据"""
    conn = pymysql.connect("111.229.170.213", "root", "123456", "cellphone")
    # 获取mysql游标
    cursor = conn.cursor()
    sql = "insert into phone_base" \
            "(base_image, base_name, base_remarks, base_feature, base_price, base_id)"\
            "values (%s, %s, %s, %s, %s, %s);"
    try:
        cursor.executemany(sql, datas)
        conn.commit()
        print("成功")
    except Exception as e:
        # 回滚数据
        conn.rollback()
        print("失败：" + sql, end="")
        print(datas)
    cursor.close()
    conn.close()
    return 1


def set_phone_one(data):
    """单个数据插入"""
    conn = pymysql.connect("111.229.170.213", "root", "123456", "cellphone")
    # 获取mysql游标
    cursor = conn.cursor()
    sql = "insert into phone_base" \
          "(base_image, base_name, base_remarks, base_feature, base_price, base_id)" \
          "values (%s, %s, %s, %s, %s, %s);"
    try:
        cursor.execute(sql, data)
        conn.commit()
        print("成功")
    except Exception as e:
        # 回滚数据
        conn.rollback()
        print("失败：", end="")
        print(data)
    cursor.close()
    conn.close()

url = "http://detail.zol.com.cn/cell_phone_index/subcate57_list_"
path = "E:/phone_image"
for i in range(1, 10):
    datas = get_phone_datas(url + str(i) + ".html")
    for data in datas:
        set_phone_one(data)
    # set_phone_mysql(datas)
