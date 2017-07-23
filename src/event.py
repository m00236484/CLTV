from datetime import datetime
import sys


class Event(object):
    
    def __init__(self, data):
       
        self.data = data
        self.eType= None
        self.eAction = None
        self.eTime = None
        self.eYear = None
        self.eWeek = None
        self.eYWeek = '00-99' #bad weekly data
        self.event_hndling()
    def __str__(self):
        return self.data
    
    def event_hndling(self):
        eTime = []
        self.eType = self.data.get('type')
        self.eAction = self.data.get('verb')
        event_time = self.data.get('event_time')
        eTime = self.time_hndling(event_time)
        if len(eTime)> 0:
            self.eTime = eTime[0]
            self.eYear = eTime[1]
            self.eWeek = eTime[2]            
            self.eYWeek = str(self.eYear)+'-'+str(self.eWeek)
        
    def time_hndling(self, event_time):
        tData = []
        DATE_FORMATS = ['%Y-%m-%dT%H:%M:%S.%fZ', '%Y-%m-%d %H:%M:%S.%fZ','%Y-%m-%d:%I:%M:%S.%fZ','%b %d %Y %I:%M%p' ,'%m/%d/%Y %I:%M:%S %p', '%Y/%m/%d %H:%M:%S', '%d/%m/%Y %H:%M', '%m/%d/%Y', '%Y/%m/%d']
        for date_format in DATE_FORMATS:
            try:
                eTime = datetime.strptime(event_time, date_format)
                year = eTime.year
                wkNumber = eTime.isocalendar()[1]                
                tData.append(eTime)
                tData.append(year)
                tData.append(wkNumber)
            except ValueError:
                print("Unexpected error:", sys.exc_info()[0])
                pass
            else:
                break 
        return tData                                    

        
