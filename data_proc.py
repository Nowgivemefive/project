# coding : utf -8

import os
from bs4 import BeautifulSoup
import pymysql
import re
'''
插入数据到Article表
'''
def insertToArticle(value):
    try:
        conn = pymysql.connect(host="127.0.0.1", port=3306, user="root", passwd="admin@155", db="xml_data",charset="utf8")
        cursor = conn.cursor()
        insert_sql = "insert into article (id, section_id, p_number,s_number,sentence,section_title, trans) values (%s, %s, %s, %s, %s, %s, %s)"
        for val in value:
            cursor.execute(insert_sql,val)
        conn.commit()
    except Exception as e:
        print(e)
    finally:
        conn.close()
'''
往表中插入数据
'''
def insertToCitation(value):
    try:
        conn = pymysql.connect(host="127.0.0.1", port=3306, user="root", passwd="admin@155", db="xml_data",charset="utf8")
        cursor = conn.cursor()
        insert_sql = "insert into citation_sentence (art_id, ref_id,s_number,cit_TYPE) values (%s, %s, %s, %s)"
        for val in value:
            cursor.execute(insert_sql,val)
        conn.commit()
    except Exception as e:
        print(e)
    finally:
        conn.close()
'''
往表中插入数据
'''
def insertToRef(value):
    try:
        conn = pymysql.connect(host="127.0.0.1", port=3306, user="root", passwd="admin@155", db="xml_data",charset="utf8")
        cursor = conn.cursor()
        insert_sql = "insert into test (id,art_id,title) value(%s, %s, %s)"
        for val in value:
            cursor.execute(insert_sql,val)
        conn.commit()
    except Exception as e:
        print(e)
    finally:
        conn.close()

def insertToRefProc():
    value =[]
    for root,dir,files in os.walk("data"):
        for file in files:
            art_id = file.split('.')[0][:8]
            with open("data/{0}".format(file),"r",encoding="utf8") as f:
                soup = BeautifulSoup(f.read(),"lxml")
                try:
                    ref_list = soup.body.references.find_all("p")
                except Exception as e:
                    continue
                for index in range(0,len(ref_list)):
                    value.append((index + 1, art_id, ref_list[index].text))
        break
    insertToRef(value)

if __name__ == '__main__':
    value = []
    citation_value = []
    for root,dir,files in os.walk("data"):
        for file in files:
            id = file.split('.')[0][:8]
            #print(id)
            with open("data/{0}".format(file),"r",encoding="utf8") as f:
                soup = BeautifulSoup(f.read(),"lxml")
                try:
                    ref_list = soup.body.references.find_all("p")
                except Exception as e:
                    continue
                for index in range(0,len(ref_list)):
                    #print(index+1, ref_list[index].text)
                    #continue
                    pass
                for section in soup.body.find_all("section"):
                    section_id = section["number"]
                    section_title = section["title"]
                    for p in section.find_all("p"):
                        #print(p.text)
                        p_number = p["number"]
                        for s in p.find_all("s"):
                            s_number =s["number"]
                            #print(id, section_id, p_number, s_number,section_title)
                            ny_list  =re.findall("\([A-Za-z\.\- ]+, [0-9]{4}[^\)]*",s.text)
                            ny2_list = re.findall("[A-Z]{1}[a-z\.\- ]+ and [A-Z]{1}[a-z\.\- ]+\([0-9]{4}\)",s.text)
                            ny3_list = re.findall("[^d] [A-Z]{1}[a-z\.\- ]+\([0-9]{4}\)",s.text)
                            if (len(ny_list) > 0 or len(ny2_list) >0 or len(ny3_list) > 0) is not True:
                                value.append((id,section_id,p_number,s_number,s.text,section_title,""))
                                #print((id,section_id,p_number,s_number,s.text,section_title,""))
                            s_content = s.text
                            if len(ny_list)>0:
                                type = "n+y"
                                for ny in ny_list:
                                    be_replace = ny+")"
                                    ref = "<"
                                    # 如果引用多人
                                    if ';' in re.sub("(\()|(\))|(,)","",ny[1:]):
                                        ref_id = 0
                                        for item in re.sub("(\()|(\))|(,)|([0-9]{4}[a-z])|([0-9]{4})|(et al.)|","",ny[1:]).split('; '):
                                            # 如果是两个人名用and连接，用if in 判断并生成 <REF ;REF>
                                            if 'and' in item:
                                                name2 = item.strip(' ').split(" and ")
                                                is_found = False
                                                for index in range(0,len(ref_list)):
                                                    if name2[0] in ref_list[index].text and name2[1] in ref_list[index].text:
                                                        ref += "REF{0};".format(index+1)
                                                        ref_id = index +1
                                                        is_found = True
                                                        break
                                            else:
                                                is_found = False
                                                if re.sub(" ",'',item) in ref_list[index].text:
                                                    ref += "REF{0};".format(index+1)
                                                    ref_id = index +1
                                                    is_found = True
                                                    break
                                        if ref!= "<":
                                            ref = ref[0:-1]
                                        if is_found:
                                            ref += ">"
                                            #print(ref)
                                            #print((id,section_id,p_number,s_number,s_content,section_title,s_content.replace(be_replace,ref)))
                                            value.append((id,section_id,p_number,s_number,s_content,section_title,s_content.replace(be_replace,ref)))
                                            citation_value.append((id,ref_id,s_number,type))
                                    else:
                                        # 如果仅引用一人或两人，就是没有用;分号连接
                                        ref = "<"
                                        #如果用and连接了
                                        ref_id = 0
                                        if "and" in re.sub("(\()|(\))|(,)|([0-9]{4})|(et al.)","",ny[1:]):
                                            name2 = re.sub("(\()|(\))|(,)|([0-9]{4})|(et al.)","",ny[1:]).split(' and ')
                                            is_found = False
                                            for index in range(0,len(ref_list)):
                                                try:
                                                    if name2[0] in ref_list[index].text and name2[1] in ref_list[index].text:
                                                        ref += "REF{0}".format(index+1)
                                                        ref_id = index +1
                                                        is_found = True
                                                        break
                                                except Exception:
                                                    if name2[0] in ref_list[index].text:
                                                        ref += "REF{0}".format(index+1)
                                                        ref_id = index +1
                                                        is_found = True
                                                        break
                                        
                                        # 如果没用and连接也就是真正的一个人
                                        else:
                                            is_found = False
                                            for index in range(0,len(ref_list)):
                                                if re.sub("(\()|(\))|(,)|([0-9]{4})|(et al.)|( )","",ny[1:]) in ref_list[index].text:
                                                    ref += "REF{0}".format(index+1)
                                                    ref_id = index +1
                                                    is_found = True
                                                    break
                                        if is_found:
                                            ref += ">"
                                            #print(ref)
                                            #print(s_content.replace(be_replace,ref))
                                            #print((id,section_id,p_number,s_number,s_content,section_title,s_content.replace(be_replace,ref)))
                                            value.append((id,section_id,p_number,s_number,s_content,section_title,s_content.replace(be_replace,ref)))
                                            citation_value.append((id,ref_id,s_number,type))
                            # 匹配一种格式的 人名
                            if len(ny2_list)>0:
                                type= "n:y"
                                ref = "<"
                                for ny2 in ny2_list:
                                    be_replace = ny2
                                    # 匹配用and连接的
                                    ref_id = 0
                                    if 'and' in re.sub("(\()|(\))|(,)|([0-9]{4})|(et al.)","",ny2[1:]):
                                        name2 = re.sub("(\()|(\))|(,)|([0-9]{4})|(et al.)","",ny2[1:]).split(' and ')
                                        is_found = False
                                        for index in range(0,len(ref_list)):
                                            try:
                                                if name2[0] in ref_list[index].text and name2[1] in ref_list[index].text:
                                                    ref += "REF{0}".format(index+1)
                                                    ref_id = index + 1
                                                    is_found = True
                                                    break
                                            except Exception:
                                                if name2[0] in ref_list[index].text:
                                                    ref += "REF{0}".format(index+1)
                                                    ref_id = index + 1
                                                    is_found = True
                                                    break
                                    else:
                                        is_found = False
                                        for index in range(0,len(ref_list)):
                                            if re.sub("(\()|(\))|(,)|([0-9]{4})|(et al.)|( )","",ny[1:]) in ref_list[index].text:
                                                ref_id = index + 1
                                                ref += "REF{0}".format(index+1)
                                                is_found = True
                                                break
                                    if is_found:
                                        ref += ">"
                                        #print(ref)
                                        #print(s_content.replace(be_replace,ref))
                                        #print((id,section_id,p_number,s_number,s_content,section_title,s_content.replace(be_replace,ref)))
                                        value.append((id,section_id,p_number,s_number,s_content,section_title,s_content.replace(be_replace,ref)))
                                        citation_value.append((id,ref_id,s_number,type))
                            # 第三种匹配
                            if len(ny3_list) > 0:
                                type = "n:y"
                                for ny3 in ny3_list:
                                    ref_id = 0
                                    be_replace = ny3[1:]
                                    #print("3",s_number,re.sub('(\()|(\))|(,)|([0-9]{4})|(et al.)','',ny3[2:]))
                                    ref = "<"
                                    is_found = False
                                    for index in range(0,len(ref_list)):
                                        if re.sub('(\()|(\))|(,)|([0-9]{4})|(et al.)','',ny3[2:]) in ref_list[index].text:
                                            ref += "REF{0}".format(index+1)
                                            ref_id = index + 1
                                            is_found = True
                                            break
                                    if is_found:
                                        ref += ">"
                                        #print(ref)
                                        #print(s_content.replace(be_replace,ref))
                                        #print((id,section_id,p_number,s_number,s_content,section_title,s_content.replace(be_replace,ref)))
                                        value.append((id,section_id,p_number,s_number,s_content,section_title,s_content.replace(be_replace,ref)))
                                        citation_value.append((id,ref_id,s_number,type))
                #print()                       
            #break # 去掉注释符只遍历一个文件
        break # 加不加都可以
    #print(len(value))
    #insertToArticle(value)
    #print(len(citation_value))
    insertToCitation(citation_value)
    print("finish")
    
