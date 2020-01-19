import pymysql
import urllib.request
import re


def create_tables():
    """创建数据表"""
    db = pymysql.connect("localhost", "root", "123456", "cellphone")
    # 获取mysql游标
    cursor = db.cursor()
    sql = "create TABLE phone" "(\
        phone_id int not NULL primary key auto_increment,\
        phone_name varchar(20),\
        base_id int foreign key references phone_base(base_id)," \
          "facade_id int foreign key references phone_facade(facade_id)," \
          "config_id int foreign key references phone_config(config_id)," \
          "show_id int foreign key references phone_show(show_id)," \
          "power_id int foreign key references phone_power(power_id)," \
          "battery_id int foreign key references phone_battery(battery_id)," \
          "camera_id int foreign key references phone_camera(camera_id)\
    );"
    cursor.execute(sql)
    print(cursor)
    cursor.close()
    db.close()


def create_data(datas, trademark):
    """增加数据"""
    conn = pymysql.connect("localhost", "root", "123456", "cellphone")
    # 获取mysql游标
    cursor = conn.cursor()
    sql = "insert into soc(soc_name, soc_trademark, soc_process, " \
          "soc_cpu_specification, soc_gpu_specification, soc_property, soc_bbx) " \
          "value(%s, " +trademark+ ", %s, %s%s, %s, %s, %s);"
    for data in datas:
        print(data)
    # datas = ('骁龙660', '14nmLPP', '四核Kryo260+四核Kryo260', '2.2+1.8GHz', 'Adreno512', '双通道LPDDR4-1866', 'X12LTECat.12/13')
    try:
        cursor.executemany(sql, datas)
        # 提交数据
        conn.commit()
    except Exception as e:
        # 回滚数据
        conn.rollback()
        print(sql)
    cursor.close()
    conn.close()
    return 1


def get_data(url):
    """网页爬取数据"""
    html = urllib.request.urlopen(url).read()
    html = html.decode("gbk")
    html = str(html)
    """裁切 从下面的文字开始"""
    html = html.split(">苹果<a")
    html = html[1]
    html = html.split(">小米<a")
    html = html[0]
    print(html)
    # 对空格回车动手
    html = html.replace("\r", "")
    html = html.replace("\n", "")
    html = html.replace(" ", "")
    html = html.replace("<br/>", "")
    html = html.replace("<p>", "")
    html = html.replace("</p>", "")
    pat = r'<tr><td>(.*?)</td><td>(.*?)</td><td>(.*?)</td><td>(.*?)</td>' \
          r'<td>(.*?)</td><td>(.*?)</td><td.*?>(.*?)</td>'
    pat = re.compile(pat)
    datas = re.findall(pat, html)
    return datas


url = "http://www.mydrivers.com/zhuanti/tianti/01/index_other.html"
datas = get_data(url)
for data in datas:
    print(data)
"""数据加品牌"""
# create_data(datas, trademark)
