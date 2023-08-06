#!/usr/bin/python
# -*- coding: utf-8 -*-\
import bs4
from bs4 import BeautifulSoup
import sys,os
reload(sys)
sys.setdefaultencoding( "utf-8" )
import json, urllib
from urllib import urlencode
import requests
#from config import *
import time
import random
from gevent import monkey; monkey.patch_all()
import gevent
import urllib2
from pyspider.conf import pyspider_host
#import hehe
#----------------------------------
# 实时IP代理库调用示例代码 － 聚合数据
# 在线接口文档：http://www.juhe.cn/docs/62
#----------------------------------
headers= {
    'Host': 'm.1688.com',
'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
'accept-encoding': 'gzip, deflate, br',
'accept-language': 'zh-CN,zh;q=0.8,en;q=0.6',
'cookie': 'UM_distinctid=15e6ed6dd7b2e-06c073d5616d11-701238-13c680-15e6ed6ddae5fc; JSESSIONID=8L788vtu1-0nHYM04zOc0TQfmxv7-wbFgsUQ-h8rA; _csrf_token=1505119984929; ctoken=VqjT3BORsax2iWjCAgsenaga; h_keys="%u7ae5%u88c5#%u5973%u88c5"; _m_h5_tk=bb17c380672e4d95e808bb534164b7c0_1505196304800; _m_h5_tk_enc=2cfa522141250a3bd9c33d63b6f51f0e; ad_prefer="2017/09/12 13:28:07"; ali_ab=113.140.248.6.1505098102710.5; CNZZDATA1261998348=1859853114-1505182966-%7C1505192053; ali-ss=eyJ1c2VySWQiOm51bGwsImxvZ2luSWQiOm51bGwsInNpZCI6bnVsbCwiZWNvZGUiOm51bGwsIm1lbWJlcklkIjpudWxsLCJzZWNyZXQiOiJXRzhSdVNKWjNFLWk3anNCLXdDaGhoZHIiLCJfZXhwaXJlIjoxNTA1MjgxMTI3NzU4LCJfbWF4QWdlIjo4NjQwMDAwMH0=; _tmp_ck_0="pgW8OZwgGvg%2FDIoFQVXmLDxmZ1BWDCaddlGOdWaOT2rvg4Up3hA%2Fw%2B99PkpLnoRjM8LJijQy%2BOzlmcIY1bxgbPsFeiyH9gz6D9nI7AiBhWXl38%2F%2F%2Bt91x9IQHD26CA9DShonSItFtED2F15sxFWlrpRY8ctSNgjHEp1Bqhm2fUwJccgs9Wq7G76KbtL892fFD9WaYAixodxWqxJxQv7TSjmemwsMIGF5yNplRhpK9ImFYU2hjDh9fv2hI%2BHYuUG%2BmvZHREL1%2BN6B%2Fejy5Op1rf3RiU%2Fj6kBAfxVxyQ2bTo%2F83jYm9jPw7Uxnb9wbeDqQQQChsQnW1Q5726RySiuESfZomfwtJ5jS"; __cn_logon__=false; cna=TZvcEaNlqAECAXGM++5Tq7Jv; webp=1; alicnweb=touch_tb_at%3D1505199489018; isg=AjY2XflYczZ7rwdQKRBlXZ65h2z4_3v5Z904uaAbw5ld49d9COZQoGLRjYl0',
'referer': 'https://m.1688.com/offer_search/-CDAFD7B0.html?spm=a26g8.7662790.0.0.3t5XoC',
'upgrade-insecure-requests': '1',
'user-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:55.0) Gecko/20100101 Firefox/55.0'
    }
def proxy_check(pro='',url='https://detail.1688.com/offer/547606605508.html?spm=a2615.7691456.0.0.SCbObK'):
    
    #print t
    try:
        # print proxie
        # pro={}
        pros = {"https":pro}
        #print pro
        # proxie.decode('utf-8').encode('utf-8')
        req = requests.get(url, proxies=pros, timeout=2,headers=headers)
        #print 'buf'
        if req.status_code==200:
            #print 'fule'
            print req.status_code

            #print req.content
          #  print req.content&toSite=main
           # print type(req.content)
            #req.encoding='gbk'
            #print req.text
            #print type(req.text)
            #reqq = bytes(bytearray(req.text, encoding='utf-8')) 
           # print reqq
            #print type(reqq)
        
            return True
        else :
            print req.status_code
            return False
    except Exception,ex:
        print Exception,":",ex
        return False
  
def main():
 
    #配置您申请的APPKey
    #appkey = "201608161557253798"
    while (True):
        try:
           
            process1()
            time.sleep(60)
        except KeyboardInterrupt,e:
            break

        except Exception,ex:
            print Exception,":",ex
            continue
 
 
#获取免费代理
def request1():
    url = "http://47.91.146.229:5080/test"
    try:

        f = requests.get(url)
    except Exception as e:
        print 'proxy ip error!' ,e
        return False

    #print type(f.content)
    return eval(f.content)
def process1():
    
    
    
    #return response.contentresponse.content.split('\r\n')
    while (1):
        rrq=request1()
        

        if rrq:

            proxy_list = rrq
            break
        else:
            print "urlmeile "
            time.sleep(5)
    
    #proxy_list=proxy_list.split('\r\n')
   
    default_conf=''
    prox=proxy_list[:-10]
    if prox:
        random.shuffle(prox)
        prox_=prox+proxy_list[-10:]
    else:
        prox_=proxy_list[-10:]

    for i in prox_:
        htt='http://'+i.strip()
        print htt
        # check=proxy_check(pro=htt)
        # print check
        # if not check:
        #     continue

            
        
        proxy = i.strip().split(':')
        proxy_conf = "cache_peer " + str(proxy[0]) + " parent " + str(proxy[1]) + " 0 login=ccc:123 round-robin proxy-only no-query connect-fail-limit=2 name="+ str(proxy[0])+ str(proxy[1]) + "\n"
        default_conf += proxy_conf
        
    conf = open('/etc/squid/peers.conf' , 'w+')
    conf.write(default_conf)
    conf.close()
    message = os.system('sudo service squid reload')
def process():
    bak = open('/etc/squid/peers.bak' , 'w+')
    proxy_list = bak.read()
    if proxy_list:
        proxy_list = eval(bak.read())
    else:
        proxy_list=[]
    #return response.contentresponse.content.split('\r\n')
    while (1):
        rrq=request1()
        

        if rrq:

            proxy_list = rrq+proxy_list
            break
        else:
            print "urlmeile "
            time.sleep(5)
    
    #proxy_list=proxy_list.split('\r\n')
    proxy_list_=[]
    default_conf=''
    for i in proxy_list:
        htt='http://'+i.strip()
        print htt
        #check=proxy_check(pro=htt)
        #print check
        #if check:
            #proxy_list_.append(i)
        
        proxy = i.strip().split(':')
        proxy_conf = "cache_peer " + str(proxy[0]) + " parent " + str(proxy[1]) + " 0 login=ccc:123 round-robin proxy-only no-query connect-fail-limit=2 name="+ str(proxy[0])+ str(proxy[1]) + "\n"
        default_conf += proxy_conf
        
    bak.write(str(proxy_list_))
    bak.close()
    conf = open('/etc/squid/peers.conf' , 'w+')
    conf.write(default_conf)
    conf.close()
    message = os.system('sudo service squid reload')

#def put_redis(r=store.connect_redis(),p=''):
    
  #  r.sadd('1',p)
    

# def request2(p=''):
#     c=''
#     m=hehe.proxies
#     if len(m)<=5:
#         time.sleep(5)
#         request1()
#     if p =='':
#         c=m[0]
#     elif p in m:
#         m.remove(p)
#         c=m[0]
#     else:
#         c=m[0]
#     #print 'yongzhegeba!' , c
#     return c
    # with open('prox', 'r') as f:
    #     lines = f.readlines()
    #     if len(lines)<=5:
    #         time.sleep(2)
    #         request1()
    #         c=request2()
    #     else:
    #         c=lines[0]
    #         wr=lines[1:]
    # with open('prox', 'w') as f:   
    #     f.writelines(wr)
    # print 'yongzhegeba!' , c
    # return c
 
if __name__ == '__main__':
    main()
