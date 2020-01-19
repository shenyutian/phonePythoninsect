import re
import urllib.request as urred
def getlink(url):
    # 模拟成浏览器
    headers = ("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36")
    opeener = urred.build_opener()
    opeener.addheaders = [headers]
    urred.install_opener(opeener)
    file = urred.urlopen(url)
    data = str(file.read())
    pat = '(https?://[^\s)";]+\.(\w|/)*)'
    link = re.compile(pat).findalls(data)
    print (link)
    link = list(set(link))
    return link

url = "http://bbs.ydss.cn/thread-1403411-1-1.html"
linklist = getlink(url)
for link in linklist:
    print (link)