import urllib,urllib2
import json
import xlsxwriter
import time

workbook = xlsxwriter.Workbook(r'C:\Users\dell\Desktop\movie.xlsx')
worksheet = workbook.add_worksheet(name='movie')

header = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
    'Origin':'https://movie.douban.com'
}

def geturl():
    urls = []
    tags = ["热门", "最新", "豆瓣高分", "冷门佳片", "华语", "欧美", "韩国", "日本"]
    for tag in tags:   
        tag = {
            'tag':tag
        }
        arg = urllib.urlencode(tag)
        url = 'https://movie.douban.com/j/search_subjects?type=movie&'+arg+'&page_limit=50&page_start='
        urls.append(url)
    return urls
rows = []
for url in geturl():
    row = len(rows)
    print 'running'
    page_start = 0
    while True:
        url2 = url
        url2 = url2 + str(page_start)
        print url2
        request = urllib2.Request(url2,headers=header)
        content = urllib2.urlopen(request,timeout=5)
        data = json.loads(content.read())
        if len(data['subjects']) == 0:
            break
        for temp in data['subjects']:
            worksheet.write(row,0,temp['id'])
            worksheet.write(row,1,temp['rate'])
            worksheet.write(row,2,temp['title'])
            worksheet.write(row,3,temp['url'])
            row = row + 1
            rows.append('0')
        page_start = int(page_start)
        page_start = page_start + 50
        time.sleep(1)
    print 'temp finish'
workbook.close()
print 'finish'
