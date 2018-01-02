#coding=utf-8

import re
import urllib.request
from bs import BeautifulSoup

import gethtml

#从天眼查网站上获取工商信息
def tianyan_search(name):
    base_url = "https://www.tianyancha.com/search?key="
    keycode = urllib.request.quote(name)
    url = base_url + keycode + "&checkFrom=searchBox"
    search_data = gethtml.get_html(url)
    search_soup = BeautifulSoup(search_data, 'html.parser')
    tag = search_soup.find('div', class_="search_right_item")
    info_url = tag.a['href']

    company_data = gethtml.get_html(info_url)
    company_data = str(company_data)
    pat = r'class="table-left">.*?</td><td .*?</td>'
    info = re.compile(pat).findall(company_data)
    pat1 = r'>[\s]*([\w-]+)[\s]*<'
    info = str(info)
    base_info = re.compile(pat1).findall(info)

    return base_info


if __name__ == '__main__':
    base_in = tianyan_search('北京百度网讯科技有限公司')
    print (base_in)

