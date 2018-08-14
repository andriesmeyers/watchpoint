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

#Call Function here
try:

  
    HttpRequest=HttpHandler.HttpHandler()
    ObjStringUtil=StringHelper.StringHelper()
    ObjDbOpertions=DBOperation.DBOperation()
    objRegularExpressionParser=RegularExpressionParser.RegularExpressionParser()
    infoLavel=Config.Config.LogLevel
    logging.info('Completed configuring logger()!')
    
    isRedirection=True
    Cookies=""
    Refer=""
    ResponseCookie=""
    redirectionURL=""
   

    url="https://www.bol.com/nl/rnwy/menu/offcanvas.html?cache=nl"
    
    HttpRequest.HttpUserAgent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36"
    HttpRequest.HttpAccept="text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8"
    HttpRequest.HttpAcceptEncoding="gzip, deflate, br"
    HttpRequest.HttpRequestHeaderName1="upgrade-insecure-requests"
    HttpRequest.HttpRequestHeaderValue1="1"
    
    objProxy=Proxy.Proxy.GetProxy(False,"","","",0,"",123)
    response=HttpRequest.HttpGetRequest(url,"GET","",Cookies,Refer,ResponseCookie,isRedirection,redirectionURL,objProxy)
    regex=r"data-px-common-categorymenu-click-name=\"Computer\s*&amp;\s*Elektronica:[\s\S]*?<a href=\"(?P<value>[\s\S]*?)\""
    CategoryURLList=ObjStringUtil.GetArrayListWithRegex(response[0],regex,1)

    nextPageURL=ObjStringUtil.GetStringResult(response[0], r"<ul\s*class=\"pagination\"", 0)
    file = open("test.txt","w") 
 
    file.write(response[0]) 
    file.close() 
    print (nextPageURL)
    print (type(nextPageURL))
except Exception as error:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            logging.error('Error in Main file!'+str(error.args))