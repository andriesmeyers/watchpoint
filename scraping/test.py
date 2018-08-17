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
    ObjStringUtil=StringHelper.StringHelper()
    ObjDbOperations=DBOperation.DBOperation()
    objRegularExpressionParser=RegularExpressionParser.RegularExpressionParser()
    infoLavel=Config.Config.LogLevel
    logging.info('Completed configuring logger()!')
    objProxy=Proxy.Proxy.GetProxy(False,"","","",0,"",123)
    isRedirection=True
    Cookies=""
    Refer=""
    ResponseCookie=""
    redirectionURL=""

    response=HttpRequest.HttpGetRequest("https://www.bol.com/nl/l/apple-laptops/N/4770+4294862300+32605/?promo=laptops_360__A_51383-51407-apple-macbooks_2_","GET","",Cookies,Refer,ResponseCookie,isRedirection,redirectionURL,objProxy)
    document = BeautifulSoup(response[0], 'html.parser')
    #ObjStringUtil.saveStringInTextFile('lastURL.txt', 'HELLO WORLD')
    
    stringtest = '/nl/l/2-in-1-laptop-azerty/N/4770+32605+28695/?promo&#x3D;laptops_360__A_51383-51384-2-in-1-laptops_1_'
    lijst = ['/nl/l/2-in-1-laptop-azerty/N/4770+32605+28695/?promo&#x3D;laptops_360__A_51383-51384-2-in-1-laptops_1_',
    '/nl/l/apple-laptops/N/4770+4294862300+32605/?promo=laptops_360__A_51383-51407-apple-macbooks_2_'
    ]
    if stringtest in lijst:
        print('gevonden')
except Exception as error:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            logging.error('Error in Main file!'+str(error.args))

