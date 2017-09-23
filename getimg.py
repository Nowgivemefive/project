import urllib2 as url2
import json
from bs4 import BeautifulSoup

f = open('img_url.txt','a') #保存图片url

# 读取首页图片url
url = 'https://www.zhihu.com/question/44187094'
req = url2.Request(url)
req.add_header('User-Agent','Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36')
response = url2.urlopen(req)  
content = response.read() #这里重复 可以写成函数
totals = content['paging']['totals']
soup = BeautifulSoup(content, 'html.parser')
img_path_list = []

# 保存首页url到txt
for imglabel in soup.find_all('img'):
    if imglabel.get("data-original") != None:
        img_path_list.append(imglabel.get("data-original"))
img_path_list = list(set(img_path_list))
for line in img_path_list:
    f.write(line)
    f.write("\n")

img_path_list = []

# 将获取的url保存到img_path_list 列表
def get_img_url(api):
    req = url2.Request(api)
    req.add_header('User-Agent','Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36')
    req.add_header('authorization','oauth c3cef7c66a1843f8b3a9e6a1e3160e20')
    response = url2.urlopen(req)  
    content = response.read()
    data = json.loads(content)
    str = ''
    for item in data['data']:
        str += item['content']
    soup = BeautifulSoup(str, 'html.parser')
    for imglabel in soup.find_all('img'):
        if imglabel.get("data-original") != None:
             img_path_list.append(imglabel.get("data-original"))
    # end of function get_img_url


offset = 23
while True:
    api = 'https://www.zhihu.com/api/v4/questions/44187094/answers?sort_by=default&include=data%5B%2A%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Cquestion%2Cexcerpt%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cupvoted_followees%3Bdata%5B%2A%5D.mark_infos%5B%2A%5D.url%3Bdata%5B%2A%5D.author.follower_count%2Cbadge%5B%3F%28type%3Dbest_answerer%29%5D.topics&limit=20&offset='
    api = '%s%d' %(api,offset)
    if( not get_img_url(api) ):
        break
    img_path_list = list(set(img_path_list)) # 去重
    for line in img_path_list:
        f.write(line)
        f.write("\n")
    img_path_list = []
    print "Running... ",
    if(offset > totals):
        break
    offset  = offset + 20


f.close()
print 'Done'
    
'''
# 下载图片
name = 1
for imgurl in img_path_list:
    req = url2.Request(imgurl)
    req.add_header('User-Agent','Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36')
    response = url2.urlopen(req)  
    content = response.read()
    with open("img/%s.jpg" %name, "wb") as f:
            f.write(content)
            print name,"has done"
            name = name + 1
'''
