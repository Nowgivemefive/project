# coding : utf-8
import urllib.request
import urllib
from bs4 import BeautifulSoup
import time
import winsound
import re

time_limit = input('设置间隔时间单位秒 例如:5 (建议高一点，防止请求过于频繁): ')
time_limit = int(time_limit)
low_limit = input('输入低于当前买价的值: ')
low_limit = float(low_limit)
high_limit = input('输入高于当前卖价的值: ')
high_limit = float(high_limit)


lowest_url = r'https://www.otcbtc.com/sell_offers?currency=gxs&fiat_currency=cny&payment_type=all'
highest_url = r'https://www.otcbtc.com/buy_offers?currency=gxs&fiat_currency=cny&payment_type=all'
headers_dict = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
    'accept-language': 'zh-CN,zh;q=0.8'
}


def get_current_low(num):
    try:
        req = urllib.request.Request(lowest_url, headers=headers_dict)
        response = urllib.request.urlopen(req, timeout=3)
        html = response.read()
        soup = BeautifulSoup(html, "html.parser")
        current_value = soup.find('span', 'price').get_text()
        current_value = current_value.replace('\n', '').strip('    ')
        lowest_data = soup.find_all('div', 'can-buy-count')[0].get_text()
        lowest_data = lowest_data.replace('\n', '').strip('    ')
        return (current_value, lowest_data)
    except Exception:
        if num == 0:
            return ('timeout','timeout')
        return get_current_low(num - 1)
def get_high(num):
    try:
        req = urllib.request.Request(highest_url, headers=headers_dict)
        response = urllib.request.urlopen(req, timeout=3)
        html = response.read()
        soup = BeautifulSoup(html, "html.parser")
        highest_data = soup.find_all('div', 'can-buy-count')[0].get_text()
        highest_data = highest_data.replace('\n', '').strip('    ')
        return highest_data
    except Exception:
        if num == 0:
            return 'timeout'
        return get_high(num -1 )

while True:
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    current_value, lowest_data = get_current_low(3)
    print('当前市价:', current_value)
    print('买价:',lowest_data)
    highest_data = get_high(3)
    print('卖价:',highest_data)

    '''
    当买价低于某个数值时
    '''
    if lowest_data != 'timeout':
        try:
            low_value = re.search('([0-9]{1,} )|([0-9]{1,}.[0-9]{1,})', lowest_data).group()
            low_value = float(low_value)
            if low_value <= low_limit:
                print('买价低于限定值{0}'.format(low_limit))
                winsound.Beep(1000, 1 * 1000)
        except Exception:
            print('网络不佳,请求超时')

    '''
    当卖价高于某个数值时
    '''
    if highest_data != 'timeout':
        try:
            high_value = re.search('([0-9]{1,} )|([0-9]{1,}.[0-9]{1,})', highest_data).group()
            high_value = float(high_value)
            if high_value >= high_limit:
                print('卖价高于限定值{0}'.format(high_limit))
                winsound.Beep(1000, 1 * 1000)
        except Exception:
            print('网络不佳,请求超时')
    print()
    time.sleep(time_limit)
