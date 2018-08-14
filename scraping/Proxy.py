import DBOperation
import pandas
import string
import Config
class Proxy():
    
    @staticmethod
    def GetProxy(serviceProxy,strProxyCategory,strCountryID, strExcludeProxyCategory, IgnoreCostGroupID,websiteName,websiteId):
        try:
            objConfig=Config.Config()
            return objConfig
        except Exception as error:
             print ('Error !!!!! %s' % error)

        



class Webproxy(object):
    def __init__(self):
        self.IP=""
        self.UserID=""
        self.Password=""
        self.ProxyCategory=""
