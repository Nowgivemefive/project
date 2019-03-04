#coding:utf8

import urllib
from urllib import request
from bs4 import BeautifulSoup
import random as rd
import re
import json


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

def get_data(page_url):
    '''
    解析文章内容
    返回一个json格式的dict
    '''
    try:
        req = urllib.request.Request(page_url, headers=headers_dict)
        response = urllib.request.urlopen(req, timeout=5)
        soup = BeautifulSoup(response.read(), "html.parser")
        push_time = project_name = soup.body.find_all("div", class_ = "vT_detail_header")[0].span.text
        #print(push_time)
        project_name = soup.body.find_all("div", class_ = "vT_detail_header")[0].h2.text
        project_name = "".join(project_name.split()).strip("\n")
        #print(project_name)
        main_content = soup.body.find_all("div",class_="vT_detail_content w100c")[0].text
        #print(main_content.text)
        data = {
            'project_name':project_name,
            'push_time':push_time,
            'main_content':main_content       
        }
        json_str = json.dumps(data)
        return json_str
    except Exception as e:
        # 处理异常
        print(e)

if __name__ == "__main__":
    data_file = open("data.txt","a")
    url = "http://www.nxgp.gov.cn/public/NXGPP/dynamic/contents/CGGG/ZBGG/index.jsp?cid=316&sid=1&page={0}"
    page_base_url = "http://www.nxgp.gov.cn/public/NXGPP/dynamic/"
    for page_num in range(0,226):
        try:
            req = urllib.request.Request(url.format(page_num), headers=headers_dict)
            response = urllib.request.urlopen(req, timeout=5)
            soup = BeautifulSoup(response.read(), "html.parser")
            table_list_table = soup.body.find_all(["table", "list_table"])[0]
            a_list = table_list_table.find_all("a",target="_blank",class_="")
            for item in a_list:
                if "医" in item.text:
                    page_url = "{0}{1}\n".format(page_base_url, item["href"])
                    #print(page_url,end="")
                    #print(item.text)
                    json_str = get_data(page_url)
                    print(page_num)
                    data_file.write("{0}\n".format(json_str))
        except Exception as e:
            # 处理异常
            print(e)
    data_file.close()
