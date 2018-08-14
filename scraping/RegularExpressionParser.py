import re
import logging as logger
import pandas as objPandas
import StringHelper
import DBOperation
import json
import urllib
from http.client import HTTPConnection
from http.client import HTTPSConnection
import HttpHandler
import Proxy 
from bs4 import BeautifulSoup

class RegularExpressionParser():
    def GetParseData(self,strResponse):
            try:
                ObjStringUtil=StringHelper.StringHelper()
                
                document = BeautifulSoup(strResponse, 'html.parser')
                ProductName = ObjStringUtil.GetStringResult(strResponse, r"<title>(?P<value>[\s\S]*?)</title>", 0);
                ProductName=str.replace(ProductName,"bol.com |","")
                EAN = ObjStringUtil.GetStringResult(strResponse, r"data-ean=\"(?P<value>[\s\S]*?)\"", 0);
                Price = ObjStringUtil.GetStringResult(strResponse, r"\"price\":(?P<value>[\s\S]*?),\"", 1);
                ImageURL = ObjStringUtil.GetStringResult(strResponse, r"data-zoom-src=\"(?P<value>[\s\S]*?)\"", 0);
                
                Categories = document.findAll("li", {"class": "specs__category"})
                
                # Get Price from Krëfel
                KreFelPrice=self.MatchBolwithKrefel(ProductName)

                # Get Price from Megekko
                MegekkoPrice=self.MatchBolwithMegekko(ProductName)

                dicData = { 
                    'ProductName': ProductName,
                    'EAN': EAN,
                    'BolPrice': Price, 
                    'KrefelPrice': KreFelPrice,
                    'MegekkoPrice': MegekkoPrice, 
                    'ImageURL': ImageURL,
                    'Categories': Categories
                }
                # dicData=(
                #     str(ProductName),
                #     str(EAN),
                #     str(Price),
                #     str(KreFelPrice),
                #     str(MegekkoPrice), 
                #     Categories,
                # ) 

                return dicData

            except Exception as error:
                logger.error("Error in RegularExpressionParser File: "+str(error))
                #print ('Error !!!!! %s' % error)

    def MatchBolwithKrefel(self,ProductName):
            try:
                ObjDbOpertions=DBOperation.DBOperation()
                ObjStringUtil=StringHelper.StringHelper()
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
                itemURL=str("https://api.krefel.be/api/v2/krefel/products/search?fields=FULL&query="+ProductName+"&currentPage=0&pageSize=1000")
                response=HttpRequest.HttpGetRequest(itemURL,"GET","",Cookies,Refer,ResponseCookie,isRedirection,redirectionURL,objProxy)

                objResponse=json.loads(str(response[0]))
                dicFinalData=[]
                ProductName=str.upper(ProductName)
                match=False
                for list in objResponse['products']:
                    Title=list['name']
                    Title=str.upper(Title)
                    brand=list['brand']['name']
                    price=list['price']['value']
                    currency=list['price']['currencyIso']
                    if Title in ProductName:
                        match=True
                        break;
                    else:
                        i=0
                        keywords=re.split(r'\s',Title)
                        length=len(keywords)
                        for key in keywords:
                            if key in ProductName:
                                i=i+1
                        #Assuming if 60% words are matched then product is matched.
                        if 100*i/length>60:
                            match=True
                            break;
                if match:
                    return price
                else: 
                    return ''
                
            except Exception as error:
                logger.error("Error in RegularExpressionParser File: "+str(error))
    def MatchBolwithMegekko(self,ProductName):
            try:
                ObjDbOpertions=DBOperation.DBOperation()
                ObjStringUtil=StringHelper.StringHelper()
                HttpRequest=HttpHandler.HttpHandler()
                HttpRequest.HttpUserAgent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36"
                HttpRequest.HttpAccept="*/*"
                #HttpRequest.HttpAcceptEncoding="gzip, deflate, br"
                HttpRequest.HttpContentType="application/x-www-form-urlencoded"
                #HttpRequest.HttpAcceptLanguage="en-US,en;q=0.9"
                
                isRedirection=True
                Cookies=""
                Refer="https://www.megekko.nl/"
                ResponseCookie=""
                redirectionURL=""
                postData=str("sid=&zoek="+ProductName.strip()+"&page=0&cache=0&navid=0&pageuri=/&navidfilter=0")
                #postData="sid=ipl15rkjc86jcr22fvbu9ltl82&zoek= Lenovo Yoga 520-14IKB 80X80055MH - 2-in-1 laptop - 14 Inch&page=0&cache=0&navid=0&pageuri=/&navidfilter=0"
                objProxy=Proxy.Proxy.GetProxy(False,"","","",0,"",123)
                itemURL=str("https://www.megekko.nl/pages/zoeken/v1.php")
                #Cookies="PHPSESSID=ipl15rkjc86jcr22fvbu9ltl82;"
                response=HttpRequest.HttpGetRequest(itemURL,"POST",postData,Cookies,Refer,ResponseCookie,isRedirection,redirectionURL,objProxy)
                
                objResponse=json.loads(str(response[0]))
                dicFinalData=[]
                ProductName=str.upper(ProductName)
                match=False
                for list in objResponse['zoek']:
                    Title=list['prodname']
                    Title=str.upper(Title)
                    price=list['price']
                    if Title in ProductName:
                        match=True
                        break;
                    else:
                        i=0
                        threshold = 90
                        keywords=re.split(r'\s',Title)
                        length=len(keywords)
                        for key in keywords:
                            if key in ProductName:
                                i=i+1
                        #Assuming if 60% words are matched then product is matched.
                        if 100*i/length>threshold:
                            match=True
                            break;
                if match:            
                    return price
                else: 
                    return ''
                
            except Exception as error:
                logger.error("Error in RegularExpressionParser File: "+str(error))
                