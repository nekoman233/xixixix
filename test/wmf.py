#! /usr/bin/env python
# coding : utf-8

from urllib.request import urlopen
from urllib.parse import urlencode
from bs4 import BeautifulSoup
import re
import json
import requests
import urllib
cookie = 'miid=943244687302250720; cna=GU/cEzHdw0oCAXALgH6Lbklq; enc=OOHf75WDH9e%2Fyb3jIcgcHGpQYeP4g5pRn2dcQriko1e9i'
'%2BEGfuOei5jNgDriTXf6Dx0HffjoAfz361L0s7VWGQ%3D%3D; thw=cn; hng=CN%7Czh-CN%7CCNY%7C156; t=29be219508acc3fe8'
'0dd5b482ab86030; uc3=vt3=F8dByR1QKxIgLrdo5t8%3D&id2=UUGq2LxDmeBy4g%3D%3D&nk2=DeJbtiq%2F4vfV&lg2=UIHiLt3xD8'
'xYTw%3D%3D; tracknick=nekoman%5Cu4E36; lgc=nekoman%5Cu4E36; cc=V32FPkk%2Fhw%3D%3D; tg=0; mt=ci=11_1&np=;'
' cookie2=33eddb22be1d3d5b77b03e97859175fb; v=0; tb_token=56b33ee3e0d5e; pnm_cku822=114%23jRCHPhCqTTobmob'
'rcW8C8%2F%2F0cO0zd%2FFcqJqsdjhGuvY8QUOHMc9zmu43EVTWRxvnmamvMkffzwTmC0UY8Wb6wbbFoJ2a3OmEvsbkT8TUo6gwTTsTnju'
'8fMoTDITaV4YjMVzpnSb7o6zmbRTTTj6Ufno9IjTsqpkwfoWnq6b82uWbJxNNPL1iq3X5NTZe%2F1IH3x7ihFzT18Aox6pgSX0LfAXjhYf'
'Ac8gYNR54EmcuB%2FR94f6k0YegViQE7b0JORk79NsS69eqeFrl1ZUz00%2F25j0gTlnEnpGOsqZmaR2wZegO9BIKcCmbib6dsjGQhtHKt'
'%2FW6mYcE%2BYgcuoqr4so6VcbIsslHcMn%2FvDGIJIVAJzAFYLQlo71NdghXCrwr; isg=BHNzJWsSKxOgt-DNmc5tFMHmAnddACxSpEE'
'vuyUQzRLJJJPGrXkJukW22xRv-F9i; x=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0%26__ll%3D-1%26_ato%'
'3D0; swfstore=138867'
header = { #这个是要访问的网址的头
"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; .NET4.0C; .NET4.0E; .NET CLR 2.0.50727; .NET "
"CLR 3.0.30729; .NET CLR 3.5.30729; InfoPath.3; rv:11.0) like Gecko",
"Aceept": 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,/;q=0.8',
"cookie": cookie
}

url = "https://yumomolk.taobao.com/search.htm?spm=a1z10.1-c-s.w5002-14519245652.1.3d1a2979oORD61&search=y"

def get_struct(url):
    req = requests.get(url, headers=header)
    req_text = BeautifulSoup(req.text,'lxml')
    # print(req_text)
    Wid = req_text.find('div',{'class': 'J_TModule'})
    print(Wid)
    wid = Wid['data-widgetid']
    print(wid) #print检测一下获得的wid是否正确
    base_url = 'https://yumomolk.taobao.com/i/asynSearch.htm?_'
    """下面这个这个网页的是请求参数表，可以用这个来写出那个request URL，
    其中_ksTS是时间戳，wid是店铺id，path是路径，
    spm是用来跟踪页面模块位置的编码"""
    params = {
                 '_ksTS': '1544164197823_264',
                 'callback': 'jsonp265',
                 'mid': 'w - 14519245696 - 0',
                 'wid': wid,
                 'path': '/ search.htm',
                 'search': 'y',
                 'spm': 'a1z10.1-c-s.w5002-14519245652.1.3d1a2979oORD61'
    }
    struct = base_url+urlencode(params)                         #拼接出数据藏匿的request URL
    return struct


def get_page(url2):
    # print(url2)
    req = requests.get(url, headers=header)
    bsObj = BeautifulSoup(req.text, "lxml")

    '''这条语句有时候能解决HTTP error 302
    (原理：默认情况下，当你进行网络请求后，响应体会立即被下载。
    你可以通过 stream 参数覆盖这个行为，推迟下载响应体)'''

    bsObj = BeautifulSoup(req.text,'lxml')
    print(req.status_code)

    "用正则来匹配所需要的内容，例如这里的"
    for link in bsObj.findAll("a",href=re.compile("/item.htm?id=\d\d\d\d\d\d\d\d\d\d\d\d")):
        # print(link)
        """我的理解：attrs把link都变成了字典形式，若字典里含有href，
        就把href所对应的值左右都去掉",然后把值赋给link1"""
        if 'href' in link.attrs:
            # print(link)
            link1 = link.attrs['href'].rstrip('\"').lstrip('\"')
            print(link1)

if __name__ == '__main__':

    """第一步，先确定爬的网址，看所需的东西到底在哪，这边是在另外一个网页上，不在源代码
    具体操作：现在网上很多淘宝店铺都是用ajax，你想找到商品在哪的话，
    谷歌浏览器，右键空白处，检查，network，all，然后选择response，
    然后一个一个点击name那里，在右边的窗口能找到你所需要的东西，找到了的话，点headers，把里面的 Request URL复制下来，
    打开这个网页，东西在这里找就好了。这里下面的URL就是真正需要的URL"""
    url = get_struct("https://yumomolk.taobao.com/search.htm?spm=a1z10.1-c-s.w5002-14519245652.1.3d1a2979oORD61&search=y")
    url2 =  get_page(url) #将get_struct()里的拼接出来的struct传入get_page().