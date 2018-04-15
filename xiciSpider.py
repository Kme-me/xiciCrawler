#-*-coding:utf-8-*-


import urllib.request
import urllib.parse
import http.cookiejar
from lxml import etree
import csv

def downloadPage(url):
    print(url)
    header={
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'max-age=0',
        'Host': 'www.xicidaili.com',
        'Proxy-Connection': 'keep-alive',
        'Referer': 'http://www.xicidaili.com/nn/2907',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36'
    }

    cookie=http.cookiejar.CookieJar()
    opener=urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookie))

    req=urllib.request.Request(url,headers=header)
    res=opener.open(req)
    print(res.code)
    if res.code==200:
        return res.read().decode('utf-8')

def constructURL(num):
    base_url="http://www.xicidaili.com/nn/%s"
    return base_url%num

def parsePage(html,f):
    f_csv=csv.writer(f)
    f_csv.writerow(['ip_addr','ip_port','ip_type'])
    html_text=etree.HTML(html)
    trs=html_text.xpath('/html/body/div[1]/div[2]/table/tr')
    del trs[0]
    for tr in trs:
        ip_addr=tr.xpath('./td[2]/text()')[0]
        ip_port=tr.xpath('./td[3]/text()')[0]
        ip_type=tr.xpath('./td[6]/text()')[0]
        f_csv.writerow([ip_addr,ip_port,ip_type])


def startCrawl(num):
    f=open('proxy.csv','w')
    for i in range(1,num+1):
        url=constructURL(i)
        html=downloadPage(url)
        parsePage(html,f)
    f.close()
    print("Finish Crwal Work...")




if __name__=='__main__':
    num_page=input("输入需要爬取的总页数：")
    num_page=int(num_page)
    startCrawl(num_page)
