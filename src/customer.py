from event import Event
from decimal import Decimal
import sys
import re
class Customer(object):
    
    def __init__(self):
        self.key = None
        self.surname = None
        self.state = None
        self.city = None 
        self.firstAction = None
        self.lastAction = None
        self.cntVisit  = 0
        self.totExpend = 0
        self.visExpend = 0
        self.cusValue  = 0
        self.wkVisits = dict()
        self.wkExpend = dict()
        self.validCustData = False
        self.segment = None
        
        self.cusLTV = 0
        self.vstExpend = 0
        self.wkVst = 0        
    
    def setCustomere(self, data):     
        if not data:
            return None

        eType   = data.get('type')
        eAction = data.get('verb')
        eTime   = data.get('event_time') 
        eYear   = data.get('event_year') 
        eWeek   = data.get('event_week')
        eYWeek  = data.get('event_YWeek')  # 99-00 bad weekly data 
        customer_id = data.get('customer_id')
        
        self.firstAction = data.get('event_time')
        self.lastAction = data.get('event_time')
        
        if eType == 'CUSTOMER':
            self.key = data.get('key')
            self.surname = data.get('last_name')
            self.state = data.get('adr_state')
            self.city = data.get('adr_city') 
            self.cntVisit  = 1
            self.totExpend = 0
            self.visExpend = 0
            self.cusValue  = 0
            self.wkVisits[eYWeek] = 1
            self.wkExpend[eYWeek]= 0
            self.validCustData = True
        else:
            self.key = data.get('customer_id')
            self.surname = 'UnKnown'
            self.state = 'UnKnown'
            self.city = 'UnKnown'
            self.cntVisit  = 1
            self.wkVisits[eYWeek] = 1
            self.validCustData = False
            if eType == 'ORDER':
                expen = data.get('total_amount')              
                self.totExpend = expen
                self.wkExpend[eYWeek] = expen
            elif eType == 'SITE_VISIT':
                self.wkExpend[eYWeek]= 0
           
            
    def updateCustomer(self, data):
        self.surname = data.get('last_name')
        self.state = data.get('adr_state')
        self.city = data.get('adr_city') 
        self.firstAction = data.get('event_time')
        self.lastAction = data.get('event_time')
        self.validCustData = True
    
    def set_customerVisit(self,eTime, eYWeek , expen ):
        
        if self.firstAction > eTime:
            self.firstAction  =eTime
           
        if self.lastAction < eTime:
            self.lastAction  =eTime           
            
        self.cntVisit  += 1
        self.totExpend +=  expen        
        if  eYWeek in self.wkVisits:
            self.wkVisits[eYWeek] += 1
        else:
            self.wkVisits[eYWeek] = 1
        if  eYWeek in self.wkExpend:
            self.wkExpend[eYWeek] += expen
        else:
            self.wkExpend[eYWeek] = expen       
        
                
    def set_custSegment(self, seg):
        self.segment = seg
        
    def set_custValue(self, cusLTV, vstExpend , wkVst):
        self.cusLTV = cusLTV
        self.vstExpend = vstExpend
        self.wkVst = wkVst
        
    def set_cntVisit(self):
        self.cntVisit += 1
        
    def set_totExpend(self, amount):
        self.totExpend += amount
        
