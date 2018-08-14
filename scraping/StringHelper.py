import re

class StringHelper():

        def GetStringResult(self,strInputText, strSearchPattern, GroupNo):
            try:
                Matches=re.findall(strSearchPattern,strInputText,re.M|re.I)
                i=0
                for Match in Matches:
                    if(i==GroupNo):
                        return Match
                    else:
                        i=i+1
            except Exception as error:
                print ('Error !!!!! %s' % error)

        def GetArrayListWithRegex(self,strInputText, strSearchPattern, GroupNo):
            try:
                Matches=re.findall(strSearchPattern,strInputText,re.M|re.I)
                return Matches
            except Exception as error:
                print ('Error !!!!! %s' % error)


        def FilterString(self,inputString, removeTags, removeWhiteSpaces):
            try:
                trimchars = { ' ', '.', ',', '?', '\'', '"', '<', '>', '*', '#' }
                if inputString:
                    inputString=str(inputString).replace("\r\n","")
                    inputString=str(inputString).replace("&nbsp;","")
                    if removeTags:
                        regularExpression = "<.+?>";
                        inputString=re.sub(regularExpression," ",inputString)
                        regularExpression = "="".+?>"
                        inputString=re.sub(regularExpression," ",inputString)
                    if removeWhiteSpaces:
                        regularExpression = "\s+"
                        inputString=re.sub(regularExpression," ",inputString)

                    inputString=str(inputString).strip(".,?\'\"<>#*")
                    inputString=str(inputString).strip(" ")
                    inputString=str(inputString).replace(", ,",",")
                
                return inputString

            except Exception as error:
                print ('Error !!!!! %s' % error)

        


