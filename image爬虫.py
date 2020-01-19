import re
import urllib.request

NETWORK_STATUS = True  # 判断状态变量


# craw 查询所有的图片路径
def craw(url, page):
    html1 = urllib.request.urlopen(url).read()
    html1 = html1.decode("gbk")
    html1 = str(html1)
    # <a href="/desk/20809.htm" title="月光奏鸣曲高清壁纸 更新时间：2018-07-02" target="_blank">
    pat2 = r'<a href="(.*?).htm" title="(.*?)" target="_blank">'
    pat2 = re.compile(pat2)
    urls = re.findall(pat2, html1)
    for url in urls:
        craw2('http://www.netbian.com'+url[0]+".htm", page)


# 真正的根据链接爬取图片
def craw2(url, page):
    # <div class="pic"><p><a href="/desk/20809-1920x1080.htm" target="_blank">
    # <img src="http://img.netbian.com/file/2018/0702/be3fd5616f0622258f29425f78a66cd6.jpg"
    # alt="月光奏鸣曲高清壁纸" title="月光奏鸣曲高清壁纸"></a></p>
    reg = r'<div class="pic"><p><a href="(.*?)" target="_blank"><img src="(.*?)" alt="(.*?)" title="(.*?)"></a></p>'
    html2 = urllib.request.urlopen(url).read()
    html2 = html2.decode("gbk")
    html2 = str(html2)
    reg = re.compile(reg)
    images = re.findall(reg, html2)
    global x
    x = 1
    for image in images:
        print(image[1])
        iname = str(image[3]).replace("","")
        imagename = "F:/爬壁纸/" + str(page) + "页" + str(iname) + ".jpg"
        try:
            urllib.request.urlretrieve(image[1], filename=imagename)
        except:
            print("错误："+image[1])
            x += 1


for i in range(1, 10):
    url = "http://www.netbian.com/erciyuan/index_"+str(i)+".htm"
    craw(url, i)
