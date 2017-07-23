from datetime import datetime
from decimal import Decimal
import sys
import re
from config import Config

class Event(object):
    
    def __init__(self):
        self.eType= None
        self.eAction = None
        self.eTime = None
        self.eYear = None
        self.eWeek = None
        self.eYWeek = '00-99' #bad weekly data

    def __str__(self):
        return self.data
    
    def getEventData(self, inEvent):
        # Return valid data
        eType = inEvent.get('type')
        if eType not in ['CUSTOMER' , 'ORDER' ,'SITE_VISIT','IMAGE']:
            # write to bad Data File
            print 'Bad Event'         
            return None
        
        event_time = self.get_event_time(inEvent.get('event_time'))
        if len(event_time) <  1:
            # write to bad Data File
            print 'Bad Event'         
            return None            
        
        data = {}    
        data['type'] = eType
        data['verb'] = inEvent.get('verb')
        data['key'] =  inEvent.get('key')
        data['customer_id'] = inEvent.get('customer_id')
        if len(event_time)> 0:
            data['event_time'] = event_time[0]
            data['event_year'] = event_time[1]
            data['event_week'] = event_time[2] 
            data['event_YWeek'] = event_time[3]         
        
        if eType == 'CUSTOMER':
            data['last_name']= inEvent.get('last_name')
            data['adr_state'] = inEvent.get('adr_state')
            data['adr_city'] = inEvent.get('adr_city')
            data['customer_id'] = inEvent.get('key')
        elif eType == 'ORDER':
            amount = self.get_amount(inEvent.get('total_amount'))
            data['total_amount'] = amount
        
        return data
          

    
    def get_amount(self, total_amount , unit = None):
      
        try:
            amount = Decimal(re.sub("[^0-9|.]", "", total_amount))  # 123456.79
        except ValueError:
            amount = 0
        if not unit:
            unit = 'D'
            
        if  str.upper(unit) == 'K' and amount <> 0 :
            amount = amount /1000
        elif str.upper(unit) == 'M'and amount <> 0 :
            amount = amount /1000000
        return amount
    
    def get_event_time(self, in_event_time):
        event_time = []
        DATE_FORMATS = ['%Y-%m-%dT%H:%M:%S.%fZ', '%Y-%m-%d %H:%M:%S.%fZ','%Y-%m-%d:%I:%M:%S.%fZ','%b %d %Y %I:%M%p' ,'%m/%d/%Y %I:%M:%S %p', '%Y/%m/%d %H:%M:%S', '%d/%m/%Y %H:%M', '%m/%d/%Y', '%Y/%m/%d']
        for date_format in DATE_FORMATS:
            try:
                eTime = datetime.strptime(in_event_time, date_format)
                eYear = eTime.year
                eWeek = eTime.isocalendar()[1]
                eYWeek = str(eYear)+'-'+str(eWeek)
                event_time.append(eTime)
                event_time.append(eYear)
                event_time.append(eWeek)
                event_time.append(eYWeek)
            except ValueError:
                print("Unexpected error:", sys.exc_info()[0])
                pass
            else:
                break 
        return event_time                                    

        
