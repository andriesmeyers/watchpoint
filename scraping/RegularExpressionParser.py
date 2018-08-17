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
                ProductName = ObjStringUtil.GetStringResult(strResponse, r"<title>(?P<value>[\s\S]*?)</title>");
                ProductName=str.replace(ProductName,"bol.com |","")
                EAN = ObjStringUtil.GetStringResult(strResponse, r"data-ean=\"(?P<value>[\s\S]*?)\"");
                Price = ObjStringUtil.GetStringResult(strResponse, r"\"price\":(?P<value>[\s\S]*?),\"");
                ImageURL = ObjStringUtil.GetStringResult(strResponse, r"data-zoom-src=\"(?P<value>[\s\S]*?)\"");
                
                Categories = document.findAll("li", {"class": "specs__category"})
                
                # Get Price from Krëfel
                KrefelPrice = self.MatchBolwithKrefelByEAN(EAN)
                if not KrefelPrice:
                    KreFelPrice=self.MatchBolwithKrefelByProdName(ProductName)

                # Get Price from Megekko
                MegekkoPrice = self.MatchBolwithMegekkoByEAN(EAN)
                if not MegekkoPrice:
                    MegekkoPrice = self.MatchBolwithMegekkoByProdName(ProductName)

                dicData = { 
                    'ProductName': ProductName,
                    'EAN': EAN,
                    'BolPrice': Price, 
                    'KrefelPrice': KreFelPrice,
                    'MegekkoPrice': MegekkoPrice, 
                    'ImageURL': ImageURL,
                    'Categories': Categories
                }

                return dicData

            except Exception as error:
                logger.error("Error in RegularExpressionParser File: "+str(error))
                #print ('Error !!!!! %s' % error)

    def MatchBolwithKrefelByEAN(self, EAN):
            try:
                # Headers
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

                # Request
                itemURL=str("https://api.krefel.be/api/v2/krefel/products/search?fields=FULL&query="+EAN+"&currentPage=0&pageSize=1000")
                response=HttpRequest.HttpGetRequest(itemURL,"GET","",Cookies,Refer,ResponseCookie,isRedirection,redirectionURL,objProxy)
                data = json.loads(str(response[0]))

                match = False
                if len(data['products']) > 0:
                    price = data['products'][0]['price']['value']
                    match = True
                
                if match:
                    return price
                else: 
                    return ''
                
            except Exception as error:
                logger.error("Error in RegularExpressionParser File: "+str(error))
    def MatchBolwithKrefelByProdName(self,ProductName):
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

                itemURL=str("https://api.krefel.be/api/v2/krefel/products/search?fields=FULL&query="+ProductName+"&currentPage=0&pageSize=1000")
                response=HttpRequest.HttpGetRequest(itemURL,"GET","",Cookies,Refer,ResponseCookie,isRedirection,redirectionURL,objProxy)

                objResponse=json.loads(str(response[0]))
                ProductName=str.upper(ProductName)
                match = False
                for list in objResponse['products']:
                    Title=list['name']
                    Title=str.upper(Title)
                    price=list['price']['value']
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
                        #Assuming if 80% words are matched then product is matched.
                        if 100*i/length>80:
                            match=True
                            break;
                if match:
                    return price
                else: 
                    return ''
                
            except Exception as error:
                logger.error("Error in RegularExpressionParser File: "+str(error))

    def MatchBolwithMegekkoByEAN(self, EAN):
            try:
                # Headers
                HttpRequest=HttpHandler.HttpHandler()
                HttpRequest.HttpUserAgent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36"
                HttpRequest.HttpAccept="*/*"
                HttpRequest.HttpContentType="application/x-www-form-urlencoded"
                
                isRedirection=True
                Cookies=""
                Refer="https://www.megekko.nl/"
                ResponseCookie=""
                redirectionURL=""
                objProxy=Proxy.Proxy.GetProxy(False,"","","",0,"",123)
                
                # Request
                postData = str("sid=&zoek="+EAN.strip()+"&page=0&cache=0&navid=0&pageuri=/&navidfilter=0")
                itemURL = str("https://www.megekko.nl/pages/zoeken/v1.php")
                response=HttpRequest.HttpGetRequest(itemURL,"POST",postData,Cookies,Refer,ResponseCookie,isRedirection,redirectionURL,objProxy)
                data = json.loads(str(response[0]))
                
                match=False
                if data['aantal'] > 0:
                    price = data['zoek'][0]['price']
                    match = True
                if match:            
                    return price
                else: 
                    return ''
                
            except Exception as error:
                logger.error("Error in RegularExpressionParser File: "+str(error))
    def MatchBolwithMegekkoByProdName(self,ProductName):
            try:
                # Headers
                HttpRequest=HttpHandler.HttpHandler()
                HttpRequest.HttpUserAgent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36"
                HttpRequest.HttpAccept="*/*"
                HttpRequest.HttpContentType="application/x-www-form-urlencoded"
                
                isRedirection=True
                Cookies=""
                Refer="https://www.megekko.nl/"
                ResponseCookie=""
                redirectionURL=""
                objProxy=Proxy.Proxy.GetProxy(False,"","","",0,"",123)
                
                # Request
                postData = str("sid=&zoek="+ProductName.strip()+"&page=0&cache=0&navid=0&pageuri=/&navidfilter=0")
                itemURL = str("https://www.megekko.nl/pages/zoeken/v1.php")
                response=HttpRequest.HttpGetRequest(itemURL,"POST",postData.encode('utf-8'),Cookies,Refer,ResponseCookie,isRedirection,redirectionURL,objProxy)
                data = json.loads(str(response[0]))
                
                ProductName=str.upper(ProductName)
                match=False
                for list in data['zoek']:
                    Title=list['prodname']
                    Title=str.upper(Title)
                    price = list['price']
                    if Title in ProductName:
                        match=True
                        break;
                    else:
                        i=0
                        threshold = 80
                        keywords=re.split(r'\s',Title)
                        length=len(keywords)
                        for key in keywords:
                            if key in ProductName:
                                i=i+1
                        #Assuming if 0% words are matched then product is matched.
                        if 100*i/length>threshold:
                            match=True
                            break;
                if match:            
                    return price
                else: 
                    return ''
                
            except Exception as error:
                logger.error("Error in RegularExpressionParser File: "+str(error))
                