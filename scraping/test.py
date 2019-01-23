import urllib
from http.client import HTTPConnection
from http.client import HTTPSConnection
import HttpHandler
import Config
import pandas
import Proxy 
import StringHelper
import DBOperation
import logging
import json
import io
import os
import sys
import time
import threading
from multiprocessing import Process

from bs4 import BeautifulSoup
from html.parser import HTMLParser

dicMegekko = {}
#Call Function here
try:

    """ HttpRequest=HttpHandler.HttpHandler()
    HttpRequest.HttpUserAgent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36"
    HttpRequest.HttpAccept="text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8"
    HttpRequest.HttpAcceptEncoding="gzip, deflate, br"
    HttpRequest.HttpRequestHeaderName1="upgrade-insecure-requests"
    HttpRequest.HttpRequestHeaderValue1="1"
    isRedirection=True
    Cookies=""
    Refer=""
    ResponseCookie=""
    redirectionURL=""
    objProxy=Proxy.Proxy.GetProxy(False,"","","",0,"",123)
    itemURL=str("https://www.artencraft.be/nl/zoeken/?text=0010343605893&category=")
    response=HttpRequest.HttpGetRequest(itemURL,"GET","",Cookies,Refer,ResponseCookie,isRedirection,redirectionURL,objProxy) """

    #document = BeautifulSoup(response[0], 'html.parser')
    #urls = ["abc", "bdc", "qdmdkj", "dqfmqskj", "mqkdjsqfdj"]
    def f(name):
        time.sleep(6)
        print(name)
    t = time.time()
    def g(name):
        print(name)
    #for url in urls:
    #    print(url)
    if __name__ == '__main__':
        p = Process(target=f, args=('bob',))
        p2 = Process(target=g, args=('robert',))

        p.start()
        p2.start()
        p.join()
        p2.join()

    print("finished in %s" % (time.time() - t))

    
        
except Exception as error:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            logging.error('Error in Test file!'+str(error.args))
