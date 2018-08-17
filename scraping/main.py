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
import math
from bs4 import BeautifulSoup

#Call Function here
try:
    
    HttpRequest=HttpHandler.HttpHandler()
    ObjStringUtil=StringHelper.StringHelper()
    ObjDbOperations=DBOperation.DBOperation()
    objRegularExpressionParser=RegularExpressionParser.RegularExpressionParser()
    infoLavel=Config.Config.LogLevel
    logging.info('Completed configuring logger()!')
    
    isRedirection=True
    Cookies=""
    Refer=""
    ResponseCookie=""
    redirectionURL=""
    # Category & Subcategory
    lastURLS = [None] * 2
    if len(sys.argv) > 1 and sys.argv[1] == "continue":
        print("\nContinuing script from last URL\n")
        # Get last URL
        with open('lastURL.txt') as f:
            lastURLS = f.read().splitlines()
            f.close()
        
    url="https://www.bol.com/nl/rnwy/menu/offcanvas.html?cache=nl"
    
    HttpRequest.HttpUserAgent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36"
    HttpRequest.HttpAccept="text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8"
    HttpRequest.HttpAcceptEncoding="gzip, deflate, br"
    HttpRequest.HttpRequestHeaderName1="upgrade-insecure-requests"
    HttpRequest.HttpRequestHeaderValue1="1"
    
    objProxy = Proxy.Proxy.GetProxy(False,"","","",0,"",123)
    response = HttpRequest.HttpGetRequest(url,"GET","",Cookies,Refer,ResponseCookie,isRedirection,redirectionURL,objProxy)
    regex = r"data-px-common-categorymenu-click-name=\"Computer\s*&amp;\s*Elektronica:[\s\S]*?<a href=\"(?P<value>[\s\S]*?)\""
    CategoryURLList = ObjStringUtil.GetArrayListWithRegex(response[0],regex)
    
    # delete previous categories
    if lastURLS[0] in CategoryURLList:
        lastCategoryIndex = CategoryURLList.index(lastURLS[0])
        del CategoryURLList[0:lastCategoryIndex]

    # Loop categories (ex. Laptops)
    for CategoryURL in CategoryURLList:
        
        lastURLS[0]     = CategoryURL
        CategoryURL     = "https://www.bol.com" + str(CategoryURL)
        response        = HttpRequest.HttpGetRequest(CategoryURL,"GET","",Cookies,Refer,ResponseCookie,isRedirection,redirectionURL,objProxy) 
        ProductBlock    = ObjStringUtil.GetStringResult(response[0], r"data-test=\"navigation-block-title\">(?P<value>[\s\S]*?)data-test=\"navigation-block-title\">")
        subCategoryURLs = ObjStringUtil.GetArrayListWithRegex(ProductBlock,r"<li>[\s\S]*?href=\"(?P<value>[\s\S]*?)\"")
        
        if subCategoryURLs is not None and len(subCategoryURLs) > 0:
            # Loop subcategories (ex. 2-in-1 Laptops)
            index = 0
            # delete previous subcategories
            if lastURLS[1] in subCategoryURLs:
                lastsubCategoryIndex = subCategoryURLs.index(lastURLS[1])
                del subCategoryURLs[0:lastsubCategoryIndex]
                print('Starting from %s' % lastURLS[1])
            else: 
                print('Last subcategory URL %s not found\n' % lastURLS[1])

            for subcategoryURL in subCategoryURLs:
                # Skip 'keuze van Bol.Com'
                if 'keuze-van' in subcategoryURL:
                    continue
                
                # add subcategory url to Last URLs
                lastURLS[1] = subcategoryURL
                ObjStringUtil.saveListInTextFile('lastURL.txt', lastURLS)

                subCategory = ObjStringUtil.GetStringResult(subcategoryURL, r"/nl/l/(?P<value>[\s\S]*?)\/")
                
                # Concat URL
                subcategoryURL="https://www.bol.com" + str(subcategoryURL)
                subcategoryURL=str.replace(subcategoryURL,"&#x3D;","=")

                # Get subcategory page
                response = HttpRequest.HttpGetRequest(subcategoryURL,"GET","",Cookies,Refer,ResponseCookie,isRedirection,redirectionURL,objProxy)

                # get Product Count
                ProductCount = ObjStringUtil.GetStringResult(response[0], r"<p\s*class=\"total-results js_total_results\"\s*data-test=\"number-of-articles\">(?P<value>[\s\S]*?)</p>");
                if ProductCount is not None:    
                    ProductCount = (str).replace(ProductCount,"resultaten","").strip()
                    ProductCount = (str).replace(ProductCount,".","").strip()
                    print(ProductCount)
                    print(type(ProductCount))
                    ProductCount = int(ProductCount)
                    print("\nScraping category: %s\n" % (subCategory))

                    # Pages Count
                    numberOfPages = 0

                    # Current Page
                    Count = 1

                    # Get number of pages
                    if ProductCount !=0 :
                        numberOfPages = ProductCount/22
                        numberOfPages = math.ceil(numberOfPages)
                    # Only crawl max of 3 pages deep
                    while Count <= numberOfPages and Count <= 3:
                        print("\nScraping page: %d" % (Count))
                        '''
                        SCRAPE PRODUCTS
                        '''
                        # Get product URLS
                        ProductURLs = ObjStringUtil.GetArrayListWithRegex(response[0], r"<a class=\"product-title\"\s*href=\"(?P<value>[\s\S]*?)\"")
                        
                        # if failed try alternative
                        if len(ProductURLs)==0:
                            ProductURLs=ObjStringUtil.GetArrayListWithRegex(response[0],r"<a class=\"product-title\s*product-title--placeholder\"\s*href=\"(?P<value>[\s\S]*?)\"")
                                        
                        # Loop products (ex. Apple MacBook Pro (2018)) 
                        for productURL in ProductURLs:
                            productURL="https://www.bol.com" + str(productURL)
                            productURL=str.replace(productURL,"&amp;","&")
                            productURL=str.replace(productURL,"&#x3D;","=")
                            product_page = HttpRequest.HttpGetRequest(productURL,"GET","",Cookies,Refer,ResponseCookie,isRedirection,redirectionURL,objProxy)
                            if productURL is not None:
                                print("\nScraping product: %s" % (productURL))
                                dicData=objRegularExpressionParser.GetParseData(product_page[0])
                                if len(dicData) > 0:
                                    ObjDbOperations.SaveDictionaryIntoMySQLDB(dicData)
                                    print("%s scraped" % (dicData['ProductName']))

                        '''
                        SCRAPE NEXT PAGE URL
                        '''

                        # Get URL for next page
                        document = BeautifulSoup(response[0], 'html.parser')
                        pagination = document.find_all("ul", {"class": "pagination"})
                        # Check for pagination
                        if pagination[0].find('li'):
                            next_page = pagination[0].find_all("li", {"class": "is-active"})[0].find_next('li').a
                            nextPageURL = next_page['href']

                            # Replace unicode
                            nextPageURL=str.replace(nextPageURL,"&amp;","&")
                            nextPageURL=str.replace(nextPageURL,"&#x3D;","=")
                            nextPageURL="https://www.bol.com" + nextPageURL

                            # Get next page
                            response=HttpRequest.HttpGetRequest(nextPageURL,"GET","",Cookies,Refer,ResponseCookie,isRedirection,redirectionURL,objProxy)
                        else: 
                            break
                        # Increment counter
                        Count += 1
            # erase last subcategory after loop finishes
            lastURLS[1] = None
            ObjStringUtil.saveListInTextFile('lastURL.txt', lastURLS)

            index += 1
    print('\n Finished scraping!')
except KeyboardInterrupt:
            print("\nScript interupted by user\n")
            sys.exit(0)
except Exception as error:               
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            logging.error('Error in Main file!'+str(error.args))
            logging.error('Line number: '+ str(exc_tb.tb_lineno))
            
def saveStringInTextFile( string ):
    text_file = open("lastURL.txt", "w")
    text_file.write(string)
    text_file.close()