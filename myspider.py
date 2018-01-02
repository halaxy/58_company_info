"""Description
- 实现抓取58同城招聘公司的信息
- 失败信息存储在当前目录下的 error.log
- python 版本：Python 3.6.0 (v3.6.0:41df79263a11, Dec 23 2016, 08:06:12)
Info
- author : "leeyoung"
- email : "reusleeyoung@163.com"
- date   : "2017.9.20"
"""
#coding=utf-8

import os
from time import ctime
from time import sleep

from  htmlparser import HtmlParser
from datastore import DataStore


class MySpider(object):
    def __init__(self, root_url):
        self.parser = HtmlParser()
        self.storage = DataStore()
        self._get_root_urls(root_url)

    def _get_root_urls(self, root_url):
        if os.path.exists('job_class.json'):
            pass
        else:
            new_urls = self.parser.get_url(root_url)
            self.storage.local_store(new_urls, 'job_class.json')#存储要爬取的行业类别url

    def joburl_init(self, pagenum, path='job_class.json'):
        root_urls = self.storage.load_data(path)
        jobs_dict ={}
        for i in pagenum:
            for list in root_urls:
                jobs_dict[list + str(i)] = root_urls[list] + str(i)#构造要爬取的网址链接
        self.storage.local_store(jobs_dict, 'job_page_url.json')#存储构造好的网址链接


    def company_url(self, path='job_page_url.json'):
        company_urls = self.storage.load_data(path)
        company_dicts ={}
        url_get = 0 #已获取的网址总数
        for company_info_url in company_urls:
            print("待爬取的行业网址总数:", len(company_urls) - url_get)
            url_get += 1
            url = company_urls[company_info_url]
            company_dicts.update(self.parser.getcompany_url(url))
            self.storage.local_store(url, 'job_page_url_old.json')#存储已爬取的网址
        self.storage.local_store(company_dicts, 'company_info_url_new.json')#存储公司信息的URL


    def company_info(self, path='company_info_url_new.json'):
        company_info_urls = self.storage.load_data(path)
        url_get = 0 #以获取的公司信息网址总数
        for company_name in company_info_urls:
            print("待爬取的公司信息网址总数:", len(company_info_urls) - url_get)
            url_get += 1
            url = company_info_urls[company_name]
            self.parser.getcompany_info(company_name, url)
            self.storage.local_store(url, 'compang_info_url_old.json')#存储以爬取的存储公司信息URL

    #从上次断点出重新开始获取公司信息
    def grab_increment(self):
        new_urls = self.storage.load_data('company_info_url_new.json')
        old_urls = self.storage.load_data('compang_info_url_old.json')
        for company_name in new_urls:
            new_url = new_urls[company_name]
            if new_url not in old_urls:
                self.parser.getcompany_info(company_name, url)
                self.storage.local_store(url, 'compang_info_url_old.json')  # 存储以爬取的存储公司信息URL

if __name__ == "__main__":
    print("开始爬取的时间：", ctime())
    root_url = 'http://sh.58.com/job.shtml'
    page_number = range(1, 50)
    sm = MySpider(root_url)
    sm.joburl_init(page_number)
    sm.company_url()
    sm.company_info()
    print("完成爬取", ctime())













