"""
- author : "leeyoung"
- email : "reusleeyoung@163.com"
- date   : "2017.9.20"
"""
#coding=utf-8

import random
import urllib.request
from time import ctime
from time import sleep

#IP池配置
IPPOOL=[
    {"ipaddr":"121.232.145.35:9000"},
    {"ipaddr":"121.232.146.184:9000"},
    {"ipaddr":"182.92.156.85:8118"},
    {"ipaddr":"117.90.4.186:9000"},
    {"ipaddr":"121.232.146.113:9000"},
    {"ipaddr":"121.232.148.25:9000"}
]

#模拟浏览器发起请求
def proxy_request(url):
    try:
        #没有找到好的代理IP
        # ip_addr = random.choice(IPPOOL)
        # proxy_ip = ip_addr["ipaddr"]
        # proxy = urllib.request.ProxyHandler({'http':proxy_ip})
        # opener = urllib.request.build_opener(proxy, urllib.request.HTTPHandler)
        # urllib.request.install_opener(opener)
        # data = urllib.request.urlopen(url).read().decode('utf-8')

        # 模拟浏览器添加报头
        req = urllib.request.Request(url)
        req.add_header("User-Agent", "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36 SE 2.X MetaSr 1.0")
        data = urllib.request.urlopen(req).read().decode('utf-8')

    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)
    except Exception as e:
        print("exception:" + str(e))
        sleep(1)

    return data

if __name__ == "__main__":
    for i in range(0,10):
        data = proxy_request("https://www.baidu.com/")
