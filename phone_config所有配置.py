import _thread

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
    sql = "select uid, url from testurl"
    cursor.execute(sql)
    datas = cursor.fetchall()
    cursor.close()
    conn.close()
    return datas


def get_data(url):
    """获取到全部数据的网站，用来获取参数列表"""
    html = urllib.request.urlopen(url).read()
    html = html.decode("gbk")
    html = str(html)
    if html.find('基本参数') != -1:
        html = html.split('>基本参数</td>')
        html = html[1]
        html = html.split("详细内容")
        html = html[0]
    else:
        html = html.split('详细参数')
        html = html[1]
        html = html.split("接下来要看")
        html = html[0]
    # html = re.sub("<a.*?/<a>", "", html)
    # pat = re.compile('>(.*?)<')
    # print("html\t", ''.join(pat.findall(html)))
    # print(html)
    # 对空格回车动手
    html = html.replace("\r", "")
    html = html.replace("\n", "")
    html = html.replace(" ", "")
    # html = html.replace("<br />", "+")
    # html = html.replace("<br/>", "+")
    # html = html.replace("<p>", "")
    # html = html.replace("</p>", "")
    # html = html.replace("></a>", "")
    # html = html.replace("</a>", "")
    html = html.replace("纠错", "")
    # 干掉空格
    html = html.replace("&nbsp;", "")
    # 对表格中的链接动手
    # html = re.sub("<ahref.*?>", "", html)
    # html = re.sub("<i.*?></i>", "", html)
    # html = re.sub("<aclass=.*?id=", "<spanid=", html)
    # html = re.sub("href.*?text=\"\">", ">", html)
    # print(html)
    regex = "<th.*?id=.*?>(.*?)</.*?></th><td.*?<spanid=\"newPmVal_([0-9]{1,2})\">(.*?)</span>.*?</td></tr>"
    # 匹配正则式
    datas = re.findall(regex, html)
    # for data in datas:
    #     print(data)
    return datas


def get_config_data(con_id, tuple_data):
    """对数据进行清洗，得到符合的列表"""
    dict_data = {0: con_id, 1: '', 2: '', 3: '', 4: '', 5: ''}
    for data in tuple_data:
        # 利用字符串替代来剔除干扰元素
        data_str = data[2]
        # 去掉 标签
        data_str = re.sub("<.*?>", "", data_str)
        data_str = re.sub("</.*?>", "", data_str)
        data_str = data_str.replace(">", "")
        if data[0] == 'CPU型号':
            dict_data[1] += (data_str + " ")
        if data[0] in ('RAM容量', 'ROM容量'):
            dict_data[2] += (data_str + " ")
        if data[0] in ('解锁方式', ''):
            dict_data[3] += (data_str + " ")
        if data[0] in ('连接与共享', '机身接口', 'NFC', 'WLAN功能', '导航', '感应器类型', '机身接口', '多媒体技术'):
            dict_data[4] += (data_str + " ")
        if data[0] in ('5G网络', '4G网络', '3G网络', '支持频段', 'SIM卡类型', '其他网络参数'):
            dict_data[5] += (data_str + " ")
    # print(dict_data)
    return list(dict_data.values())


def set_config_mysql(listdatas):
    """增加配置信息数据  listdatas 数据集"""
    conn = pymysql.connect(sqlName, "root", "123456", "cellphone")
    # 获取mysql游标
    cursor = conn.cursor()

    # 防止插入失败，所以先删表
    cursor.execute("DELETE FROM phone_config")

    sql = "insert into phone_config" \
          "(config_id, soc_name, config_memory, config_unlock, config_networking, config_remork) "\
          "values (%s, %s, %s, %s, %s, %s);"
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


def get_facade_data(con_id, tuple_data):
    """对数据进行清洗，得到符合的列表"""
    dict_data = {0: con_id, 1: '', 2: '', 3: '', 4: ''}
    for data in tuple_data:
        # 利用字符串替代来剔除干扰元素
        data_str = data[2]
        # 去掉 标签
        data_str = re.sub("<.*?>", "", data_str)
        data_str = re.sub("</.*?>", "", data_str)
        data_str = data_str.replace(">", "")
        if data[0] == '手机尺寸':
            dict_data[1] += (data_str + " ")
        if data[0] == '手机重量':
            dict_data[2] += (data_str + " ")
        if data[0] == '机身材质':
            dict_data[3] += (data_str + " ")
        if data[0] == '其他外观参数':
            dict_data[4] += (data_str + " ")
    # print(dict_data)
    return list(dict_data.values())


def set_facade_mysql(listdatas):
    """增加数据  facade_id外观id  listdata 数据"""
    conn = pymysql.connect(sqlName, "root", "123456", "cellphone")
    # 获取mysql游标
    cursor = conn.cursor()

    cursor.execute("DELETE FROM phone_facade")

    sql = "insert into phone_facade" \
          "(facade_id, facade_size, facade_weight, facade_texture, facade_other) "\
          "values (%s, %s, %s, %s, %s);"
    try:
        #  2阶 sql语句
        cursor.executemany(sql, listdatas)
        conn.commit()
    except Exception as e:
        # 回滚数据
        conn.rollback()
        print("失败：" + sql)
    cursor.close()
    conn.close()
    return 1


def get_show_data(show_id, tuple_data):
    """对数据进行清洗，得到符合的屏幕参数列表"""
    dict_data = {'ID': show_id, 'texture': '', 'size': '', 'resolratio': '', 'arrange': '',
                 'ppi': '', 'aod': '', 'colorControl': '', 'maxLuinance': '', 'stimulateLuminance': '',
                 'colorTem': '', 'srgb': '', 'p3': '', 'quality': '', 'other': ''}
    for data in tuple_data:
        # 利用字符串替代来剔除干扰元素
        data_str = data[2]
        # 去掉 标签
        data_str = re.sub("<.*?>", "", data_str)
        data_str = re.sub("</.*?>", "", data_str)
        data_str = data_str.replace(">", "")
        if data[0] == '主屏尺寸':
            dict_data['size'] += data_str
        if data[0] == '主屏材质':
            dict_data['texture'] += data_str
        if data[0] == '主屏分辨率':
            dict_data['resolratio'] += data_str
        if data[0] == '屏幕像素密度':
            dict_data['ppi'] += data_str
        if data[0] in ('窄边框', 'HDR技术', '屏幕占比', '屏幕技术'):
            dict_data['other'] += (data[0] + ":" + data_str + " ")
        if data[0] == '其他屏幕参数':
            dict_data['other'] += (data_str + " ")
    # print(dict_data)
    return list(dict_data.values())


def set_show_mysql(listdatas):
    """增加屏幕信息数据  listdatas 数据集"""
    conn = pymysql.connect(sqlName, "root", "123456", "cellphone")
    # 获取mysql游标
    cursor = conn.cursor()

    cursor.execute("DELETE FROM phone_show")

    sql = "insert into phone_show" \
          " " \
          "values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
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


def get_battery_data(bat_id, tuple_data):
    """对数据进行清洗，得到符合的电池参数列表"""
    dict_data = {'ID': bat_id, 'capacity': '', 'scheme': '', 'cableCharger': '', 'wirelessCharger': '',
                 'cableTime': '', 'wirelessTime': '', 'endurance': '', 'other': ''}
    for data in tuple_data:
        # 利用字符串替代来剔除干扰元素
        data_str = data[2]
        # 去掉 标签
        data_str = re.sub("<.*?>", "", data_str)
        data_str = re.sub("</.*?>", "", data_str)
        data_str = data_str.replace(">", "")
        if data[0] == '电池容量':
            dict_data['capacity'] += data_str
        if data[0] == '续航时间':
            dict_data['endurance'] += data_str
        if data[0] == '电池充电':
            dict_data['scheme'] += data_str
        if data[0] == '其他硬件参数':
            dict_data['other'] += data_str
    # print(dict_data)
    return list(dict_data.values())


def set_battery_mysql(listdatas):
    """增加电池信息数据  listdatas 数据集"""
    conn = pymysql.connect(sqlName, "root", "123456", "cellphone")
    # 获取mysql游标
    cursor = conn.cursor()

    # cursor.execute("DELETE FROM phone_battery")
    # conn.commit()

    sql = "insert into phone_battery" \
          " " \
          "values (%s, %s, %s, %s, %s, %s, %s, %s, %s);"
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


def get_camera_data(camera_id, tuple_data):
    """对数据进行清洗，得到符合的相机参数列表"""
    dict_data = {'ID': camera_id, 'amount': '', 'cmos': '', 'pixel': '', 'focalLength': '',
                 'aperture': '', 'ois': '', 'fosusing': '', 'graph': '', 'video': '',
                 'steadyVideo': '', 'slowMotion': '', 'remarks': ''}
    for data in tuple_data:
        # 利用字符串替代来剔除干扰元素
        data_str = data[2]
        # 去掉 标签
        data_str = re.sub("<.*?>", "", data_str)
        data_str = re.sub("</.*?>", "", data_str)
        data_str = data_str.replace(">", "")
        if data[0] == '摄像头总数':
            dict_data['amount'] += data_str
        if data[0] == '传感器型号':
            dict_data['cmos'] += data_str
        if data[0] in ('前置摄像头', '后置摄像头', '摄像头特色', '广角'):
            dict_data['pixel'] += (data[0] + ":" + data_str + " ")
        if data[0] == '焦距/范围':
            dict_data['focalLength'] += data_str
        if data[0] == '光圈':
            dict_data['aperture'] += data_str
        if data[0] == '拍照功能':
            dict_data['graph'] += data_str
        if data[0] == '视频拍摄':
            dict_data['video'] += data_str
        if data[0] == '其他摄像头参数':
            dict_data['remarks'] += (data_str + " ")
    # print(dict_data)
    return list(dict_data.values())


def set_camera_mysql(listdatas):
    """增加相机信息数据  listdatas 数据集"""
    conn = pymysql.connect(sqlName, "root", "123456", "cellphone")
    # 获取mysql游标
    cursor = conn.cursor()

    cursor.execute("DELETE FROM phone_camera")

    sql = "insert into phone_camera" \
          " " \
          "values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
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


def set_datas_file(phone_id, tuple_data):
    """清洗保存全部数据"""
    listdata = [phone_id]
    file.write(str(phone_id))
    file.write("\r\n")
    for data in tuple_data:
        # 利用字符串替代来剔除干扰元素
        data_str = data[2]
        # 去掉 标签
        data_str = re.sub("<.*?>", "", data_str)
        data_str = re.sub("</.*?>", "", data_str)
        data_str = data_str.replace(">", "")
        listdata.append((data[0], data_str))
        print(data[0])
        file.write(data[0])
        file.write("\t")
        file.write(data_str)
        file.write("\r\n")
    file.write("\r\n")
    print("listdata\t", listdata)
    return listdata


""" url = "http://detail.zol.com.cn/1282/1281307/param.shtml" """
"""1070996 有异常"""
datas = get_data_forsqlurl()
# 二阶列表，存放需要的数据集
listdatas = []
# 写入文件中
file = open('F:\\zgc_phone.txt', 'w')
i = 0
for data in datas:
    config_id = data[0]
    # 1070996, 1271058 有问题 先跳过
    # if config_id == 1270996 or config_id == 1271058:
        # continue
    # 拼接得到真正的链接
    url = ''.join(data[1])
    print("url\t", url)
    data = get_data(url)

    # 清洗数据 并且保存在listdatas中
    # listdatas.append(set_datas_file(config_id, data))
    """需要什么数据就去执行 下面的选项"""
    # 获取数据 自动按照类型判定 这是保存配置数据
    # listdatas.append(tuple(get_config_data(config_id, data)))
    # listdatas.append(tuple(get_battery_data(config_id, data)))
    # listdatas.append(tuple(get_camera_data(config_id, data)))
    # listdatas.append(tuple(get_facade_data(config_id, data)))
    # listdatas.append(tuple(get_show_data(config_id, data)))
    # if i < 2:
    #     i += 1
    # else:
    #     break
print(listdatas)
# 写入数据库
# set_config_mysql(listdatas)
# set_battery_mysql(listdatas)
# set_camera_mysql(listdatas)
# set_facade_mysql(listdatas)
# set_show_mysql(listdatas)
# 关闭文件
file.close()

