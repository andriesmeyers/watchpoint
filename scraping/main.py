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
    # Loop categories
    for item in CategoryURLList:
        itemURL="https://www.bol.com" + str(item)
        response=HttpRequest.HttpGetRequest(itemURL,"GET","",Cookies,Refer,ResponseCookie,isRedirection,redirectionURL,objProxy) 
        ProductBlock = ObjStringUtil.GetStringResult(response[0], r"data-test=\"navigation-block-title\">(?P<value>[\s\S]*?)data-test=\"navigation-block-title\">", 0);
        ProductCategoryURLs=ObjStringUtil.GetArrayListWithRegex(ProductBlock,r"<li>[\s\S]*?href=\"(?P<value>[\s\S]*?)\"",1)
        
        # Loop subcategories
        for subcategoryURL in ProductCategoryURLs:
            print("Scraping category with url %s" % (subcategoryURL))
            
            # Concat URL
            subcategoryURL="https://www.bol.com" + str(subcategoryURL)
            subcategoryURL=str.replace(subcategoryURL,"&#x3D;","=")
            
            # Get subcategory page
            response=HttpRequest.HttpGetRequest(subcategoryURL,"GET","",Cookies,Refer,ResponseCookie,isRedirection,redirectionURL,objProxy)
            
            # Get URL for next page
            nextPageURL = ObjStringUtil.GetStringResult(response[0], r"<ul\s*class=\"pagination\"\s*data-test=\"pagination\">[\s\S]*?<a href=\"(?P<value>[\s\S]*?)\"", 0)
            
            # Get product URLS
            ProductURLs = ObjStringUtil.GetArrayListWithRegex(response[0], r"<a class=\"product-title\"\s*href=\"(?P<value>[\s\S]*?)\"", 1)
            
            # if failed try alternative
            if len(ProductURLs)==0:
                ProductURLs=ObjStringUtil.GetArrayListWithRegex(response[0],r"<a class=\"product-title\s*product-title--placeholder\"\s*href=\"(?P<value>[\s\S]*?)\"",1)
            
            # get Product Count
            ProductCount= ObjStringUtil.GetStringResult(response[0], r"<p\s*class=\"total-results js_total_results\"\s*data-test=\"number-of-articles\">(?P<value>[\s\S]*?)</p>", 0);
            ProductCount=(str).replace(ProductCount,"resultaten","").strip()
            
            # Loop product urls
            for productURL in ProductURLs:
                    # Concat URL
                    itemURL="https://www.bol.com" + str(productURL)
                    itemURL=str.replace(itemURL,"&amp;","&")
                    itemURL=str.replace(itemURL,"&#x3D;","=")
                    
                    # Product Page
                    response=HttpRequest.HttpGetRequest(itemURL,"GET","",Cookies,Refer,ResponseCookie,isRedirection,redirectionURL,objProxy)
                    
                    # Get product details
                    dicData=objRegularExpressionParser.GetParseData(response[0])
                    
                    # Save in database
                    if len(dicData) > 0:
                        ObjDbOpertions.SaveDictionaryIntoMySQLDB(dicData)
                        print("%s scraped" % (dicData[0]))
                    
            pCount=int(ProductCount)
            nPaging=0
            Count=2
            # Replace unicode
            nextPageURL=str.replace(nextPageURL,"&amp;","&")
            nextPageURL=str.replace(nextPageURL,"&#x3D;","=")
            # Get page numbers
            if(pCount !=0):
                nPaging=pCount/20
            for item in ProductURLs:
                itemURL="https://www.bol.com" + str(item)
                itemURL=str.replace(itemURL,"&#x3D;","=")
                response=HttpRequest.HttpGetRequest(itemURL,"GET","",Cookies,Refer,ResponseCookie,isRedirection,redirectionURL,objProxy)
                dicData=objRegularExpressionParser.GetParseData(response[0])
                print("%s scraped" % (dicData[0]))
            
            # Only crawl max of 3 pages deep
            while Count <= nPaging or Count > 3:
                page="page="+str(Count)
                nxtPageURL=str.replace(nextPageURL,"page=2",page)
                nxtPageURL="https://www.bol.com" + nxtPageURL
                response=HttpRequest.HttpGetRequest(nxtPageURL,"GET","",Cookies,Refer,ResponseCookie,isRedirection,redirectionURL,objProxy)
                ProductURL=ObjStringUtil.GetArrayListWithRegex(response[0],r"<a class=\"product-title\"\s*href=\"(?P<value>[\s\S]*?)\"",1)
                
                if len(ProductURL)==0:
                    ProductURL=ObjStringUtil.GetArrayListWithRegex(response[0],r"<a class=\"product-title\s*product-title--placeholder\"\s*href=\"(?P<value>[\s\S]*?)\"",1)
                for item in ProductURL:
                    itemURL="https://www.bol.com" + str(item)
                    itemURL=str.replace(itemURL,"&amp;","&")
                    itemURL=str.replace(itemURL,"&#x3D;","=")
                    response=HttpRequest.HttpGetRequest(itemURL,"GET","",Cookies,Refer,ResponseCookie,isRedirection,redirectionURL,objProxy)
                    dicData=objRegularExpressionParser.GetParseData(response[0])
                    if len(dicData) > 0:
                        ObjDbOpertions.SaveDictionaryIntoMySQLDB(dicData)
                        print("%s scraped" % (dicData[0]))
                Count += 1
                ## Only scrape 5 pages
                if(Count==5):
                    break
except KeyboardInterrupt:
            print('Script interrupted by user')
            sys.exit(0)
except Exception as error:               
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            logging.error('Error in Main file!'+str(error.args))
            logging.error('Line number: '+ exc_tb.tb_lineno)
