import re

class StringHelper():

        def GetStringResult(self,strInputText, strSearchPattern):
            try:
                Matches=re.findall(strSearchPattern,strInputText,re.M|re.I)
                for Match in Matches:
                    return Match
            except Exception as error:
                print ('Error: %s' % error)

        def GetArrayListWithRegex(self,strInputText, strSearchPattern):
            try:
                Matches=re.findall(strSearchPattern,strInputText,re.M|re.I)
                return Matches
            except Exception as error:
                print ('Error: %s' % error)


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
                print ('Error: %s' % error)

        
        def saveListInTextFile(self, filename, stringList ):
            try:
                text_file = open(filename, "w")
                for string in stringList:
                    text_file.write("%s\n" % string)
                text_file.close()
            except Exception as error:
                print('Error: %s' % error)

