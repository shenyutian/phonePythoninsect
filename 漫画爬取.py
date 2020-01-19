import urllib.request
import re

def geturl(url) :
    """获取漫画的url和章节名称"""
    html = urllib.request.urlopen(url).read()
    html = html.decode("gbk")
    html = str(html)
    htmls = html.split("class=\"Drama autoHeight\">")
    html = htmls[1]
    html = html.split("class=\"img_001 globalPadding globalbottom10\">")
    html = html[0]
    # print(html)
    pat = " href=\"(.*?)\"><span>(.*?)</span>"
    pat = re.compile(pat)
    datas = re.findall(pat, html)
    # for data in datas:
        # print(data)
    return datas[1:]

def getimage(data) :
    """网页获取图片，然后保存"""
    for i in (1, 2):
        url = data[0] + "?p=" + str(i)
        print(url)
        html = urllib.request.urlopen(url).read()
        html = html.decode("gbk")
        html = str(html)
        html = html.split("漫画图片")
        html = html[1]
        html = html.split("王牌御史")
        html = html[0]
        print(html)
        pat = "src=\"(.*?.jpg)"
        pat = re.findall(pat, html)
        print(pat)



# url = "http://www.517mh.net/wap/comic/10133/276080.html?p=13"
# http://www.517mh.net/wap/comic/10133/276072.html
# http://www.517mh.net/wap/comic/10133/276071.html
url = "http://www.517mh.net/wap/comic/10133/"
datas = geturl(url)
for data in datas:
    getimage(data)
    break

