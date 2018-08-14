import urllib
from http.client import HTTPConnection
from http.client import HTTPSConnection
from urllib.parse import urlparse,urlencode
import Config as objConfig
import requests
import ast
from requests.auth import HTTPDigestAuth
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
#import string as Headers

#import HTTPRequestHeaders as ObjRequestHeader
class HttpHandler():
    def __init__(self):
        self.HttpAccept=""
        self.HttpUserAgent=""
        self.HttpContentType=""
        self.HttpAcceptEncoding=""
        self.HttpAcceptLanguage=""
        self.HttpRequestHeaderName1=""
        self.HttpRequestHeaderValue1=""
        self.HttpRequestHeaderName2=""
        self.HttpRequestHeaderValue2=""
        self.HttpRequestHeaderName3=""
        self.HttpRequestHeaderValue3=""
        self.HttpRequestHeaderName4=""
        self.HttpRequestHeaderValue4=""
        self.HttpRequestHeaderName5=""
        self.HttpRequestHeaderValue5=""

    
    # Function Get Response definition is here
    def HttpGetRequest(self,URL,HitType,PostDetail,Cookies,Refer,ResponseCookie,isRedirection,redirectionURL,objProxy):
        verify='/etc/ssl/certs/cacert.org.pem'
        try:
            headers=self.CreateHeaders()
            #if PostDetail:
                #postData=self.CreatePostData(PostDetail)
            if not objProxy==None:
                if(str(objConfig.Config.UseProxy).upper()=="TRUE"):
                    if(len(objProxy)>0):
                        if(objProxy[9] !=""):
                            strproxies = {
                                "http": "http://"+objProxy[9]+":"+objProxy[10]+"@"+objProxy[3]+"/",
                                "https": "https://"+objProxy[9]+":"+objProxy[10]+"@"+objProxy[3]+"/",
                            }
                        else:
                            strproxies = {
                                "http": "http://"+objProxy[3]+"/",
                                "https": "https://"+objProxy[3]+"/",
                            }
            
            #auth = HTTPDigestAuth(objProxy[9], objProxy[10])
            if str(objConfig.Config.UseProxy).upper()=="FALSE":
               strproxies=None
            if str(objConfig.Config.UseProxy).upper()=="TRUE":
               if objProxy==None:
                    response="No Proxy Return"
                    return response
            if(HitType.upper()=="GET"):
                ObjResponse = requests.get(URL, headers=headers, proxies=strproxies, allow_redirects=isRedirection,timeout=int(objConfig.Config.RegexTimeOut),verify=False)
            else:
                ObjResponse = requests.post(URL, data=PostDetail, headers=headers, proxies=strproxies,allow_redirects=isRedirection,timeout=int(objConfig.Config.RegexTimeOut),verify=False)
        
            response=ObjResponse.text
            
            if 'Location' in ObjResponse.headers:
                redirectionURL=ObjResponse.headers['Location']

            statuscode=ObjResponse.status_code

            if 'set-cookie' in ObjResponse.headers._store:
                for cookie in ObjResponse.headers._store['set-cookie']:
                    if not cookie=="Set-Cookie":
                        ResponseCookie += cookie + "; "
            
            #ResponseCookie += cookie.name + "=" + cookie.value + "; "
            #ResponseCookie=ObjResponse.headers._store['set-cookie'][1]
            return response,ResponseCookie,redirectionURL
        except Exception as error:
            print ('Error !!!!! %s' % error)


    def CreateHeaders(self):
        try:
            Headers="{"
        
            if(self.HttpAccept !=""):
                Headers=Headers+"\"Accept\": " + "\""+self.HttpAccept + "\""  
            if (self.HttpContentType !=""):
                Headers=Headers+","+"\"Content-type\": " + "\""+self.HttpContentType + "\""    
            if (self.HttpUserAgent !=""):
                Headers=Headers+","+"\"User-Agent\": " + "\""+self.HttpUserAgent + "\""
            if (self.HttpAcceptLanguage !=""):
                Headers=Headers+","+"\"Accept-Language\": " + "\""+self.HttpAcceptLanguage + "\""   
            if (self.HttpAcceptEncoding !=""):
                Headers=Headers+","+"\"Accept-Encoding\": " + "\""+self.HttpAcceptEncoding + "\""
            if (self.HttpRequestHeaderName1 !="" and self.HttpRequestHeaderValue1 !=""):
                Headers=Headers+","+"\""+self.HttpRequestHeaderName1+"\": " + "\""+self.HttpRequestHeaderValue1 + "\""
            if (self.HttpRequestHeaderName2 !="" and self.HttpRequestHeaderValue2 !=""):
                Headers=Headers+","+"\""+self.HttpRequestHeaderName2+"\": " + "\""+self.HttpRequestHeaderValue1 + "\""
            if (self.HttpRequestHeaderName3 !="" and self.HttpRequestHeaderValue3 !=""):
                Headers=Headers+","+"\""+self.HttpRequestHeaderName3+"\": " + "\""+self.HttpRequestHeaderValue1 + "\""
            if (self.HttpRequestHeaderName4 !="" and self.HttpRequestHeaderValue4 !=""):
                Headers=Headers+","+"\""+self.HttpRequestHeaderName4+"\": " + "\""+self.HttpRequestHeaderValue1 + "\""
            if (self.HttpRequestHeaderName5 !="" and self.HttpRequestHeaderValue5 !=""):
                Headers=Headers+","+"\""+self.HttpRequestHeaderName5+"\": " + "\""+self.HttpRequestHeaderValue1 + "\""

            Headers=Headers+"}"
            Headers=ast.literal_eval(Headers)
            return Headers  
        except Exception as error:
            print ('Error !!!!! %s' % error)

    # end function HttpGetRequest
    # Convert post data from string into dictionary
    def CreatePostData(self,postData):
        dPostData = {}
        for pair in postData.replace(' ','').split('&'):
            k, v = pair.split('=')
            dPostData[k] = v
        #postDetail=dPostData
        return dPostData


    
 
    