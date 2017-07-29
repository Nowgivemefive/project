#!/bin/bash
# download.sh
if [ ! $1 ]
then
	echo 'need question url'
	exit 1
fi

ques_num=`echo $1 | egrep -o '[0-9]+'`

function gethtml()
{
    curl --user-agent 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36' -H 'authorization: oauth c3cef7c66a1843f8b3a9e6a1e3160e20' $1
}
gethtml $1 | egrep -o 'data-original="[^"]*' | egrep -o 'https://[^ ]*'| sort |uniq >> $$.log

api="https://www.zhihu.com/api/v4/questions/${ques_num}/answers?sort_by=default&include=data%5B%2A%5D.is_normal%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Cmark_infos%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cupvoted_followees%3Bdata%5B%2A%5D.author.follower_count%2Cbadge%5B%3F%28type%3Dbest_answerer%29%5D.topics&limit=20&offset="


offset=3
total=`gethtml $api$offset | egrep -o '"totals": [0-9][^,]*' | egrep -o '[0-9]+'`
total=`expr $total + 20`
api_html=''
for((offset=3;offset<$total;offset+=20))
do
    api_html=`echo $api${offset}`
    gethtml $api_html| egrep -o 'data-original=\\"[^\]*' | egrep -o 'https://[^ ]*'|sort|uniq>>$$.log &
done
wait
echo 'get img url complete'

max_th=50 #指定最大线程数
# 线程控制
function getimg()
{
	if [[ $max_th -ge $((`ps | grep download.sh | wc -l` - 1)) ]] # 减一是前去‘grep fileme'的行
	then
        {       
               wget $url
        }&
	else
        	getimg
	fi

}

# 下载图片
for url in `cat $$.log`
do
	getimg
done
wait
echo 'downlad complete'
