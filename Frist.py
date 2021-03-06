# @Author :tangzhong
# -*-codeing = utf-8 -*-
# @time : 2021/6/19 16:13
# @File :test.py
# @Software:
import re
import sqlite3
import urllib.request

import xlwt
from bs4 import BeautifulSoup


def main():

    # 1、爬取网页
    baseurl = 'https://movie.douban.com/top250?start='

    # 2、解析数据
    datalist = getData(baseurl)
    # print(datalist)

    # 3、保存数据到表格
    savepath = "豆瓣电影TOP250.xls"
    saveData(datalist,savepath)
    #4、保存数据到sql
    dbpath= "douban.db"
    saveDatadb(datalist,dbpath)


# 正则表达式
# 匹配影片详情link
findLink = re.compile(r'<a href="(.*?)">')  # 创建正则表达式对象，表示规则
# 图片link
fimdImgSrc = re.compile(r'<img.*src="(.*?)"', re.S)  # 让换行符号包含在字符中
# 电影片名
findTitle = re.compile(r'<span class="title">(.*?)</span>', re.S)
# 电影评分
findRating = re.compile(r'<span class="rating_num" property="v:average">(.*?)</span>', re.S)
# 电影评价人数
findJudge = re.compile(r'<span>(\d*)人评价</span>', re.S)
# 电影概况
findInq = re.compile(r'<span class="inq">(.*?)</span>', re.S)
# 电影相关内容
findBd = re.compile(r'<p class="">(.*?)</p>', re.S)


def getData(baseurl):
    datalist = []
    for i in range(0, 25):
        url = baseurl + str(i * 25)
        # 1、请求网页数据
        html = askURL(url)
        #print(html)
        # 2、逐一解析数据
        soup = BeautifulSoup(html, 'html.parser')
        for item in soup.find_all('div', class_="item"):
            data = []
            item = str(item)
            # 电影链接
            link = re.findall(findLink, item)[0]
            data.append(link)
            # 图片链接
            imgSrc = re.findall(fimdImgSrc, item)[0]
            data.append(imgSrc)

            # 电影名称
            titles = re.findall(findTitle, item)
            if len(titles) == 2:
                ctitle = titles[0]
                data.append(ctitle)
                otitle = titles[1].replace(" / ", "")  # 替换掉斜杠
                data.append(otitle)
            else:
                data.append(titles[0])
                data.append('')  # 空外文名

            # 电影评分
            rating = re.findall(findRating, item)[0]
            data.append(rating)

            # 电影评价人数
            judge = re.findall(findJudge, item)[0]
            data.append(judge)

            # 添加概述
            inq = re.findall(findInq, item)
            if len(inq) != 0:
                inq = inq[0].replace('。', '')
                data.append(inq)
            else:
                data.append('')
            #处理多余字符
            bd = re.findall(findBd, item)[0]
            bd = re.sub('<br/(\s+)?>(\s+)', ' ', bd)
            bd = re.sub('/', ' ', bd)
            bd = re.sub('\xa0', '', bd)
            data.append(bd.strip())
            datalist.append(data)
    print("一共{}条数据".format(len(datalist)))
    return datalist


# 获取一个网页数据
def askURL(url):
    head = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36 Edg/90.0.818.46',
        'Cookie': 'bid=DC4HOPgHgYk; douban-fav-remind=1; ll="118154"; _vwo_uuid_v2=D55D8789A6CB1C0141B7AB8F5F46F2DEA|432450a16bb89113c2ea522ae2dff42f; dbcl2="116480524:Jk9DUusBYYY"; ck=-cYx; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1619399989%2C%22https%3A%2F%2Faccounts.douban.com%2F%22%5D; _pk_id.100001.4cf6=30965674262a4003.1619314590.3.1619399989.1619324803.; _pk_ses.100001.4cf6=*; __utma=30149280.104439603.1611802597.1619324803.1619399990.5; __utmb=30149280.0.10.1619399990; __utmc=30149280; __utmz=30149280.1619399990.5.4.utmcsr=accounts.douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; __utma=223695111.1482137965.1619314590.1619324803.1619399990.3; __utmb=223695111.0.10.1619399990; __utmc=223695111; __utmz=223695111.1619399990.3.2.utmcsr=accounts.douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; push_noty_num=0; push_doumail_num=0'}
    # httpproxy_handler = urllib.request.ProxyHandler({"http": "114.239.145.124:9999"})
    # opener = urllib.request.build_opener(httpproxy_handler)
    request = urllib.request.Request(url, headers=head)
    html = ""
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode()
    except urllib.error.URLError as e:
        if hasattr(e, "e"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)
    return html


# 保存数据到表格
def saveData(datalist,savepath):
    workbook = xlwt.Workbook(encoding='utf-8', style_compression=0)  # 创建工作簿
    worksheet = workbook.add_sheet('豆瓣电影TOP250', cell_overwrite_ok=True)  # 创建工作表
    col = ("电影详情链接", "图片链接", "中文名", "外文名", "评分", "评价数", "概况", "相关信息")
    for i in range(0, 8):
        worksheet.write(0, i, col[i])

    for i in range(0, 250):
        print("第{}条".format(i + 1))
        data = datalist[i]
        for j in range(0, 8):
            worksheet.write(i + 1, j, data[j])

    workbook.save(savepath)


# 保存数据到sql
def saveDatadb(datalist,dbpath):
    init_db()
    conn=sqlite3.connect("douban.db")
    cur=conn.cursor()

    for data in datalist:
        for index in range(len(data)):
            data[index]='"'+data[index]+'"'
        sql='''
                insert into movie250(
                info_link,pic_link,cname,ename,score,rated,instroduction,info)
                values(%s)'''%",".join(data)
        cur.execute(sql)
        conn.commit()
    cur.close()
    conn.close()

def init_db():
    sql='''
        create table movie250
        (id integer primary key autoincrement,
        info_link text,
        pic_link text,
        cname varchar,
        ename varchar,
        score numeric,
        rated numeric,
        instroduction text,
        info text
        )'''
    conn=sqlite3.connect("douban.db")
    cursor=conn.cursor()
    cursor.execute(sql)
    conn.commit()
    conn.close()
if __name__ == "__main__":
    main()
    print("over")