# coding : utf-8

'''
爬取怀俄明大学 探空数据
程序的目的是 实现这个下载过程 https://jingyan.baidu.com/article/1e5468f900536e484961b73e.html
数据所在的网页 http://weather.uwyo.edu/upperair/sounding.html
这个程序仅下载中国地区站点的数据
'''
'''
你可以把这个程序当做简单的爬虫练习
'''
# 导入需要的库
import os
import urllib
from urllib import request
from bs4 import BeautifulSoup
import random as rd
import time

# 自定 user-agent, 模仿用户行为 
user_agent = ['Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
              'Mozilla/5.0(Windows;U;WindowsNT6.1;en-us)AppleWebKit/534.50(KHTML,likeGecko)Version/5.1Safari/534.50',
              'Mozilla/4.0(compatible;MSIE7.0;WindowsNT5.1;TencentTraveler4.0)',
              'User-Agent:Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
              'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0']
# 随机选择user-agent
headers_dict = {
    'User-Agent': rd.choice(user_agent),
}
# 下载1973-2017年份数据，这里可以用更简洁的方法写， 比如用range
year_list = [1973, 1974, 1975, 1976, 1977, 1978, 1979, 1980, 1981, 1982, 1983, 1984, 1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017]
# url
url = "http://weather.uwyo.edu/cgi-bin/sounding?region=seasia&TYPE=TEXT%3ALIST&YEAR={0}&MONTH={1}&FROM=0100&TO={2}12&STNM={3}"
# 月份列表
mouth_list = ["01","02","03","04","05","06","07","08","09","10","11","12"]
# point.txt中存的是 中国大陆上的点
f = open("point.txt","r")
for line in f:
    #对站点和月份 分类放置数据
    station = line[:5]
    if not os.path.exists("data"):
        os.mkdir("data")
    if not os.path.exists("data/{0}".format(station)):
        os.mkdir("data/{0}".format(station))
    '''
    根据闰年或平年或月份选择天数
    '''
    for year in year_list:
        for mouth in mouth_list:
            day = 30
            if mouth in ["01","03","05","07","08","10","12"]:
                day = 31
            if mouth == "02":
                if (year%4==0 and year%100 != 0) or year%400==0:
                    day = 29
                else:
                    day = 28
            data_file = "data/{0}/{1}{2}.txt".format(station,year,mouth)
            print(url.format(year, mouth, day,station))
            #if os.path.exists(data_file):
            #    continue
            # 构造请求, 爬取数据
            try:
                req = urllib.request.Request(url.format(year, mouth, day,station), headers=headers_dict)
                response = urllib.request.urlopen(req, timeout=60)
                soup = BeautifulSoup(response.read(), "html.parser")
                res_list = soup.body.find_all(["h2", "pre"])
                if len(res_list) > 0:
                    file = open(data_file, "w", encoding="utf8")
                    for item in res_list:
                        file.write(item.text)
                    file.close()
            except Exception as e:
                # 处理异常
                print(e)
                time.sleep(0.1* 60)
                error_log = open("error.txt", "a")
                error_log.write(url.format(year, mouth, day,station))
                error_log.write("\n")
                error_log.close()
