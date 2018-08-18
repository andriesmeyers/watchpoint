import urllib
from http.client import HTTPConnection
from http.client import HTTPSConnection
import HttpHandler
import Config
import pandas
import Proxy 
import StringHelper
import RegularExpressionParser
import DBOperation
import logging
import json
import io
import os
import sys
from bs4 import BeautifulSoup

#Call Function here
try:
    HttpRequest=HttpHandler.HttpHandler()
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
    # itemURL=str("https://www.artencraft.be/nl/zoeken/?text=0018208949021")
    # response=HttpRequest.HttpGetRequest(itemURL,"GET","",Cookies,Refer,ResponseCookie,isRedirection,redirectionURL,objProxy)

    # document = BeautifulSoup(response[0], 'html.parser')
    # products = document.findAll("ul", {"class": "product-overview"})
    # product = products[0].find("strong", {"class": "product-price"}).get_text()
    # print(product.replace('€', ''))

    # # match=False

    # # if len(data['products']) > 0:
    # #     print(data['products'][0]['price']['value'])
    
except Exception as error:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            logging.error('Error in Main file!'+str(error.args))

