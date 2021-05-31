# @Author :tangzhong
# -*-codeing = utf-8 -*-
# @time : 2021/5/30 14:42
# @File :小唐出版.py
# @Software:
from bs4 import BeautifulSoup #网页解析，获取数据
import re   #正则表达式，进行文字匹配
import urllib.request,urllib.error  #制定url，获取网页数据
import xlwt #进行excel操作
import sqlite3   #进行sqlite数据库操作
#爬取网页，解析数据，保存数据

def main():
    print("开始爬......................")
    baseurl = "http://www.cwrank.com/main/rank.php?geo=all&page="
    #爬取数据
    datalist = getData(baseurl)
    savepath = '全球排名榜.xls'
    #保存数据
    saveData(datalist,savepath)

#爬取网页
def getData(baseurl):
    datalist =[]
    for i in range(1,11):#调用获取页面信息的函数，10次
        #print(i)
        url = baseurl + str(i)
        print(url)
        html =askURL(url)#保存获取的网页源码
        #print(html)
    #逐一解析数据
    soup=BeautifulSoup(html,"html.parser")
    #print(soup)
    for top in soup.find_all('td',valign="top"):#查找符合要求的字符串，形成列表
        #print(top)#测试查看top全部信息
        data = []#保存一部电影的所以信息
        top = str(top)
        #获取影片详情的链接
        #1排名
        paiming= re.findall(re.compile(r'<tr bgcolor="(ffffff|#F2F8E7)" height="15"><td align="center" class="main">(.*?)</td>'),top)[0]  # re库用来通过正则表达式查找指定的字符串
        #print(paiming)
        data.append(paiming)
        #2站名
        zhanming= re.findall(re.compile(r'<td align="left" class="main"><a href="(.*?)" target="_blank" title="(.*?)">(.*?)</a></td>'),top)[0]
        #print(zhanming)
        data.append(zhanming)
        #3地区
        diqu= re.findall(re.compile(r'<td align="center" class="main"><a href="?.geo=(.*?)">(.*?)</a></td>'),top)[0]
        #print(diqu)
        data.append(diqu)
        #4类别
        leibie= re.findall(re.compile(r'<td align="center" class="main"><a href="?.type=(.*?)">(.*?)</a></td>'),top)[0]
        #print(leibie)
        data.append(leibie)
        #5本周排名
        week= re.findall(re.compile(r'<td align="center" class="main">(.*?)></td><td align="center" class="main">(.*?)</td><td align="center" class="main">(.*?)</td>'),top)[0]
        #print(week)
        data.append(week)
    datalist.append(data)
    return datalist



#得到指定一个URL的网页内容
def askURL(url):
    head = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36",'Cookie': 'bid=DC4HOPgHgYk; douban-fav-remind=1; ll="118154"; _vwo_uuid_v2=D55D8789A6CB1C0141B7AB8F5F46F2DEA|432450a16bb89113c2ea522ae2dff42f; dbcl2="116480524:Jk9DUusBYYY"; ck=-cYx; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1619399989%2C%22https%3A%2F%2Faccounts.douban.com%2F%22%5D; _pk_id.100001.4cf6=30965674262a4003.1619314590.3.1619399989.1619324803.; _pk_ses.100001.4cf6=*; __utma=30149280.104439603.1611802597.1619324803.1619399990.5; __utmb=30149280.0.10.1619399990; __utmc=30149280; __utmz=30149280.1619399990.5.4.utmcsr=accounts.douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; __utma=223695111.1482137965.1619314590.1619324803.1619399990.3; __utmb=223695111.0.10.1619399990; __utmc=223695111; __utmz=223695111.1619399990.3.2.utmcsr=accounts.douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; push_noty_num=0; push_doumail_num=0'
            }#伪装，伪装自己
    request = urllib.request.Request(url,headers=head)
    html=" "
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode("utf-8")
        #print(html)
    except urllib.error.URLError as e:
        if hasattr(e,"code"):
            print(e.code)
        if hasattr(e,"reason"):
            print(e.reason)
    return html


def saveData(datalist,savepath):
    print("保存中.........")
    book= xlwt.Workbook(encoding="utf-8")  # 创建workbook对象
    sheet = book.add_sheet("全球排名榜",cell_overwrite_ok=True)  # 创建工作表
    col = ("排名","站名","地区","类别","本周排名以及上周排名和月访问量")
    for i in range(0,5):
        sheet.write(0,i,col[i])
    for i in range(0,5):
        print("第%d条"%(i+1))
        data = datalist[i]
        for j in range(0,5):
            sheet.write(i+1,j,data[j])

    book.save(savepath)


if __name__=="__main__":
    main();
    print("成功了")