import sys
import os
from datetime import datetime

class Config(object):
    def __init__(self):
        self.logName = None
        self.outPutDir = None
        self.outFile = self.set_outFile('output')
    def writeOutput(self,data):
        outFile = self.outFile
        f= open(outFile,"w+")
        if type(data) == type(str()):
            f.writelines(data)
        elif type(data) == type(dict()):
            for line in data:
                f.write(line)
                f.write(data(line))
        elif type(data) == type(list()):
            for line in data:
                f.write(str(line)+'\n')          
        else:
            raise ValueError
        
        
        f.close()     
        
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
    
def main():
    import os
    conf = Config()
    print conf.set_outFile('output')
    

if __name__ == '__main__':
    main() 