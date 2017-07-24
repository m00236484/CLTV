import sys
import os
from datetime import datetime

class Config(object):
    def __init__(self):
        self.logName = None
        self.outPutDir = None
        self.outFile = self.set_outFile('output')
    def writeOutput(self,outFile,data, isLog = None ):
        headtext = ''
        outTxt = ''
        if isLog == True:
            headtext = str(datetime.now()) +'\t'

        f= open(outFile,"a")
        if type(data) == type(str()):
            outTxt = headtext + str(data)  + '\n'
            f.writelines(outTxt)
        elif type(data) == type(dict()):
            for line in data:
                outTxt = headtext + str(line) + '\t'
                f.write(outTxt)
                f.write(data(line))
        elif type(data) == type(list()):
            for line in data:
                outTxt = headtext + str(line) +'\n'
                f.write(outTxt)          
        else:
            raise ValueError
        f.close()     
        return outFile
    
    def set_outFile(self, fileType):
        fileTime = datetime.now().strftime("%m%d%Y-%I%M%S")
        outFile = fileType + '_' + fileTime+'.txt'
        outPath =  self.set_outPutDir()
        outFile =  os.path.join(outPath,outFile)
        return outFile
    
    def set_outPutDir(self):
        dir = os.path.dirname(os.getcwd())
        path = os.path.join(dir,'output')
        if not os.path.exists(path):
            os.makedirs(path)                    
        return path
    
