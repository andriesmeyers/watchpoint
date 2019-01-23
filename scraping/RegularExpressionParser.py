import re
import sys
import os
import logging
import pandas as objPandas
import StringHelper
import DBOperation
import json
import urllib
import time
from multiprocessing import Process, Manager
from http.client import HTTPConnection
from http.client import HTTPSConnection
import HttpHandler
import Proxy 
from bs4 import BeautifulSoup

class RegularExpressionParser():
    
    def GetParseData(self,strResponse, productURL):
        try:
            ObjStringUtil=StringHelper.StringHelper()
            document    = BeautifulSoup(strResponse, 'html.parser')
            manager     = Manager()
            ProductName = ObjStringUtil.GetStringResult(strResponse, r"<title>(?P<value>[\s\S]*?)</title>")
            ProductName = str.replace(ProductName,"bol.com |","")
            EAN         = ObjStringUtil.GetStringResult(strResponse, r"data-ean=\"(?P<value>[\s\S]*?)\"")
            Price       = ObjStringUtil.GetStringResult(strResponse, r"\"price\":(?P<value>[\s\S]*?),\"");
            Price       = Price.replace('.', '')
            Price       = Price.replace(',', '.')
            Price       = Price.replace('-', '')
            ImageURL    = ObjStringUtil.GetStringResult(strResponse, r"data-zoom-src=\"(?P<value>[\s\S]*?)\"")
            SpecTitles  = ObjStringUtil.GetArrayListWithRegex(strResponse, r"class=\"specs__title\">(?P<value>[\s\S]*?)<")
            SpecValues  = ObjStringUtil.GetArrayListWithRegex(strResponse, r"class=\"specs__value\">(?P<value>[\s\S]*?)<")
            Categories  = document.findAll("li", {"class": "specs__category"})
            Description = document.findAll("div", {"class": "product-description"})
            dicSpecs    = {}
            
            for i in range(len(SpecTitles)):
                title = SpecTitles[i].strip()
                # Skip categorieën
                if(title == "Categorie&euml;n"):
                    break
                value = SpecValues[i].strip()
                dicSpecs[title] = value
            if Description:
                Description = Description[0].encode_contents()
                Description = str.replace(Description.decode("utf-8") ,"'","\\n")
            
            dicBol = {
                "price": Price,
                "url": productURL
            }
            dicKrefel = manager.dict()
            dicMegekko = manager.dict()
            dicArtnCraft = manager.dict()
            
            # 
            # Multiprocessing
            #
         
            krefelProcess = Process(target=self.FetchDicKrefel, args=(EAN, ProductName, dicKrefel))
            megekkoProcess = Process(target=self.FetchDicMegekko, args=(EAN, ProductName, dicMegekko))
            artnCraftProcess = Process(target=self.FetchDicArtnCraft, args=(EAN, ProductName, dicArtnCraft))
            
            # start processes
            krefelProcess.start()
            megekkoProcess.start()
            artnCraftProcess.start()

            # wait for processes to complete
            krefelProcess.join()
            megekkoProcess.join()
            artnCraftProcess.join()

            krefelProcess.close()
            megekkoProcess.close()
            artnCraftProcess.close()

            dicData = { 
                'ProductName': ProductName,
                'EAN': EAN,
                'Description': Description,
                'Specs': dicSpecs,
                'Bol': dicBol,
                'Krefel': dicKrefel['value'],
                'Megekko': dicMegekko['value'],
                'ArtandCraft': dicArtnCraft['value'],
                'ImageURL': ImageURL,
                'Categories': Categories
            }
            return dicData

        except Exception as error:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            logging.error('Error in RegularExpressionParser file!'+str(error.args))
            logging.error('Line number: '+ str(exc_tb.tb_lineno))

    def FetchDicKrefel(self, EAN, ProductName, dic):
        try:
            # Get Price from Krëfel
            print("\nScraping Krëfel")
            
            dicKrefel = self.MatchBolwithKrefelByEAN(EAN)

            if dicKrefel is None:
                dicKrefel = self.MatchBolwithKrefelByProdName(ProductName)
            
            if dicKrefel is not None:
                print('Price found for Krefel: € %s' % dicKrefel["price"])
            
            dic['value'] = dicKrefel
        except Exception as error:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            logging.error("Error in RegularExpressionParser File: "+str(error.args))
            logging.error('Line number: '+ str(exc_tb.tb_lineno))

    def FetchDicMegekko(self, EAN, ProductName, dic):
        try:
            # Get Price from Megekko
            print("\nScraping Megekko")
        
            dicMegekko = self.MatchBolwithMegekkoByEAN(EAN)
        
            if dicMegekko is None:
                dicMegekko = self.MatchBolwithMegekkoByProdName(ProductName)

            if dicMegekko is not None:
                print('Price found for Megekko: € %s' % dicMegekko["price"])
            
            dic['value'] = dicMegekko   
        except Exception as error:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            logging.error("Error in RegularExpressionParser File: "+str(error.args))
            logging.error('Line number: '+ str(exc_tb.tb_lineno))

    def FetchDicArtnCraft(self, EAN, ProductName, dic):
        try:
           
            # Get Price from Art & Craft
            print("\nScraping Art & Craft")
            
            dicArtnCraft = self.MatchBolwithArtandCraftByEAN(EAN)

            if dicArtnCraft is not None:
                print('Price found for Art & Craft: € %s' % dicArtnCraft["price"])
            
            dic['value'] = dicArtnCraft
        except Exception as error:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            logging.error("Error in RegularExpressionParser File: "+str(error.args))
            logging.error('Line number: '+ str(exc_tb.tb_lineno))

    def MatchBolwithKrefelByEAN(self, EAN):
            try:
                dicKrefel = {}
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
                    dicKrefel['price'] = data['products'][0]['price']['value']
                    dicKrefel['url'] = "https://www.krefel.be/" + data['products'][0]['url']
                    match = True
                
                if match:
                    return dicKrefel
                else: 
                    return None
                
            except Exception as error:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                logging.error("Error in RegularExpressionParser File: "+str(error.args))
                logging.error('Line number: '+ str(exc_tb.tb_lineno))
    def MatchBolwithKrefelByProdName(self,ProductName):
            try:
                dicKrefel = {}
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
                    Title = list['name']
                    Title = str.upper(Title)
                    dicKrefel["price"] = list['price']['value']
                    dicKrefel["url"] = "https://www.krefel.be/" + list['url']
                    if ProductName in Title:
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
                    return dicKrefel
                else: 
                    return None
                
            except Exception as error:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                logging.error("Error in RegularExpressionParser File: "+str(error.args))
                logging.error('Line number: '+ str(exc_tb.tb_lineno))
    def MatchBolwithMegekkoByEAN(self, EAN):
            try:
                dicMegekko = {
                    'price': '',
                    'url': ''
                }
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
                    dicMegekko["price"] = data['zoek'][0]['price']
                    dicMegekko["url"] = "https://www.megekko.nl" + data['zoek'][0]['link'].strip()
                    match = True
                if match:            
                    return dicMegekko
                else: 
                    return None
                
            except Exception as error:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                logging.error("Error in RegularExpressionParser File: "+str(error.args))
                logging.error('Line number: '+ str(exc_tb.tb_lineno))
    def MatchBolwithMegekkoByProdName(self,ProductName):
            try:
                dicMegekko = {}
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
                match = False
                for list in data['zoek']:
                    Title=list['prodname']
                    Title=str.upper(Title)
                    dicMegekko['price'] = list['price']
                    dicMegekko['url'] = "https://www.megekko.nl" + list['link'].strip()
                    if ProductName in Title:
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
                    return dicMegekko
                else: 
                    return None
                
            except Exception as error:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                logging.error("Error in RegularExpressionParser File: "+str(error))
                logging.error('Line number: '+ str(exc_tb.tb_lineno))

                
    def MatchBolwithArtandCraftByEAN(self, EAN):
        try:
            dicArtnCraft = {}

            # Headers
            HttpRequest=HttpHandler.HttpHandler()
            HttpRequest.HttpUserAgent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36"
            HttpRequest.HttpAccept="*/*"
            HttpRequest.HttpContentType="application/x-www-form-urlencoded"
            
            isRedirection=True
            Cookies=""
            Refer=""
            ResponseCookie=""
            redirectionURL=""
            objProxy=Proxy.Proxy.GetProxy(False,"","","",0,"",123)
            
            # Request
            params = str("?text=" + EAN)
            itemURL = str("https://www.artencraft.be/nl/zoeken/" + params)
            response = HttpRequest.HttpGetRequest(itemURL,"POST",params,Cookies,Refer,ResponseCookie,isRedirection,redirectionURL,objProxy)
            document = BeautifulSoup(response[0], 'html.parser')

            match = False
            products = document.findAll("ul", {"class": "product-overview"})
            if products is not None and len(products) > 0:
                price = products[0].find("strong", {"class": "product-price"}).get_text()
                price = price.replace('€', '')
                price = price.replace('.', '')
                price = price.replace(',', '.')
                price = price.replace('-', '')
                dicArtnCraft["price"] = price
                url = products[0].find('div', {'class': 'product-data-top-wrap'}).a
                dicArtnCraft["url"] = "https://www.artencraft.be/" + url['href']

                match = True
            if match:            
                return dicArtnCraft
            else: 
                return None
            
        except Exception as error:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            logging.error("Error in RegularExpressionParser File: "+str(error))
            logging.error('Line number: '+ str(exc_tb.tb_lineno))
