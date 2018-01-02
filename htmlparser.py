"""
- author : "leeyoung"
- email : "reusleeyoung@163.com"
- date   : "2017.9.20"
"""
#coding=utf-8

import re
import urllib.request
from time import ctime,sleep
from bs4 import BeautifulSoup

import proxy
from datastore import DataStore
from mylog import Logger


class HtmlParser(object):

    #获取工作种类的url
    def get_url(self, start_url):
        logger = Logger(logname='error.log', logger="58com").getlog()
        url_dict = {}
        try:
            data = proxy.proxy_request(start_url)
            soup = BeautifulSoup(data, 'html.parser')
            tags = soup.find(id="sidebar-right")
            tags_li = tags.find_all('li')
            for tag in tags_li:
                a_tags = tag.find_all('a')
                job_class = a_tags[0].string
                job_urlname = a_tags[0].attrs.get('href')
                ##处理相对路径和绝对路径
                if job_urlname.startswith('/'):
                    job_urlname = "http://bj.58.com" + job_urlname + "pn"
                    url_dict[job_class] = job_urlname
                else:
                     url_dict[job_class] = job_urlname

        except urllib.error.URLError as e:
            if hasattr(e, "code"):
                print(e.code)
            if hasattr(e, "reason"):
                print(e.reason)
            logger.error("Can not open start url: %s", start_url)
        except Exception as e:
            print("exception:" + str(e))
            sleep(1)

        return url_dict

    #获取某招聘公司信息的url
    def getcompany_url(self, job_url):
        logger = Logger(logname='error.log', logger="58com").getlog()
        company_list ={}
        try:
            data = proxy.proxy_request(job_url)
            soup = BeautifulSoup(data, 'html.parser')
            tags = soup.find_all('div', class_="comp_name")
            for tag in tags:
                company_name = tag.a.get_text()
                company_url = tag.a['href']
                #处理相对路径和绝对路径
                if company_url.startswith('http'):
                    company_list[company_name] = company_url
                else:
                    company_list[company_name] = "http://qy.58.com" + company_url

        except urllib.error.URLError as e:
            if hasattr(e, "code"):
                print(e.code)
            if hasattr(e, "reason"):
                print(e.reason)
            logger.error("get compang url failed, url: %s", job_url)#记录失败日志
        except Exception as e:
            print("exception:" + str(e))
            sleep(1)

        return company_list

    #获取招聘公司的基本信息和工商信息
    def getcompany_info(self, name, url):
        logger = Logger(logname='error.log', logger="58com").getlog()
        ds = DataStore()
        try:
            company_text = []
            html = proxy.proxy_request(url)
            soup = BeautifulSoup(html, 'html.parser')
            tag = soup.find(class_="basicMsg")
            ul = tag.find("ul")
            li_tags = ul.find_all(name='li')
            strinfo = re.compile('\s')
            for li in li_tags:
                txt = strinfo.sub('', li.get_text())
                company_text.append(txt.split('：')[1])
            #获取工商信息
            #gongshang_info = tianyan.tianyan_search(name)
            #gongshang_info = ','.join(gongshang_info)
            ds.insert_database(name, company_text)

        except urllib.error.URLError as e:
            if hasattr(e, "code"):
                print(e.code)
            if hasattr(e, "reason"):
                print(e.reason)
            logger.error("Get company info fail, company name: %s, url: %s", name, url)#记录解析失败的公司和url
        except Exception as e:
            print("exception:" + str(e))
            sleep(1)

if __name__ == "__main__":
    start_url = "http://sh.58.com/job.shtml"
    html_par = html_parser()
    #获取要爬取的工作列表
    jobs_list = html_par.get_url(start_url)
    #获取公司信息url
    company_dict = html_par.getcompany_url(jobs_list)
    #获取公司信息存储至数据库
    for name, url in company_dict.items():
        html_par.getcompany_info(name, url)

