import sys
import json
import unittest
from decimal import Decimal
import re
from customer import Customer
from event import Event
from config import Config

class CLTV(object):
     
    def __init__(self, fileName):
           
        self.customers = {}
        self.cusLTVs = {}
        self.loadJson(fileName)
        self.analysis()
        self.analysis_dateFrame()
        
        
    def loadJson(self, fileName):
        
        if fileName:
            with open(fileName, 'r') as f:
                objects = json.load(f)
            if len(objects)>1:
                for event in objects:
                    self.ingest(event) 
        else:
            return None
        
    def ingest(self, event):
        data = Event().getEventData(event)
        if not data:
            return None
            
        eType   = data.get('type')
        eAction = data.get('verb')
        eTime   = data.get('event_time') 
        eYear   = data.get('event_year') 
        eWeek   = data.get('event_week')
        eYWeek  = data.get('event_YWeek')  # 99-00 bad weekly data 
        customer_id = data.get('customer_id')
        if eType == 'CUSTOMER':
            customer_id = data.get('key')
            if customer_id in self.customers  :
                #update customer Detail 
                if self.customers.get(customer_id).validCustData :
                    self.customers.get(customer_id).updateCustomer(data)             
            else:
                customer = Customer()
                self.customers[customer_id] = customer
                self.customers.get(customer_id).setCustomere(data)  
        
        #print self.customers
        else:
            if customer_id not in self.customers:
                customer = Customer()
                self.customers[customer_id] = customer
                self.customers.get(customer_id).setCustomere(data)             
            else:
                if eType == 'SITE_VISIT':
                    self.customers.get(customer_id).set_customerVisit(eTime, eYWeek , 0 )
                elif eType == 'ORDER':
                    expen = data.get('total_amount')
                    self.customers.get(customer_id).set_customerVisit(eTime, eYWeek , expen )
                    
              
    def analysis1(self):
        vistExpe = 0
        wkVisit = 0
        cusCount = len(self.customers.keys())
        print cusCount
        for key  in self.customers:
            print self.customers.get(key).cntVisit   

    def analysis(self):
        vistExpe = 0
        wkVisit = 0
        cusCount = len(self.customers.keys())
        for key  in self.customers:
            #print self.customers.get(key).totExpend
            cusVstExpe = self.customers.get(key).totExpend / self.customers.get(key).cntVisit
            vistExpe += cusVstExpe 
            cusVstWklV = self.customers.get(key).cntVisit / len(self.customers.get(key).wkVisits.keys())
            wkVisit += cusVstWklV  
            wkCustVal = vistExpe * wkVisit
            cusLTV = 52 * wkCustVal * 10
            self.cusLTVs[key] = cusLTV
        avrVistExpe  = vistExpe /  cusCount
        avrWkVisit   = wkVisit / cusCount
        avrcusLTV    = 52 * (avrVistExpe * avrWkVisit) * 10 
    
    def analysis_dateFrame(self):
        vistExpe = 0
        wkVisit = 0
        cusCount = len(self.customers.keys())
        for key  in self.customers:
            #print self.customers.get(key).totExpend
            cusVstExpe = self.customers.get(key).totExpend / self.customers.get(key).cntVisit
            vistExpe += cusVstExpe 
            
            firstAction = self.customers.get(key).firstAction 
            lastAction =  self.customers.get(key).lastAction
            Weeks = (lastAction-firstAction).days / 7
            cusVstWklV = self.customers.get(key).cntVisit / Weeks
            wkVisit += cusVstWklV  
            wkCustVal = vistExpe * wkVisit
            cusLTV = 52 * wkCustVal * 10
            self.cusLTVs[key] = cusLTV
        avrVistExpe  = vistExpe /  cusCount
        avrWkVisit   = wkVisit / cusCount
        avrcusLTV    = 52 * (avrVistExpe * avrWkVisit) * 10 
        
    def TopXSimpleLTVCustomers(self,x):
       #outputFile = conf.set_outFile('outpu')
        conf = Config()
        data = []
        topX = 0
        if int(x) <= len(self.cusLTVs.keys()):
            
            topX = x
        else:
            topX = len(self.cusLTVs.keys())
            print('Requested Top Clients > Count of Clients')

        for w in sorted(self.cusLTVs, key=self.cusLTVs.get, reverse=True)[:int(topX)]:
            datao = str(w) + "\t"+ str(self.customers.get(w).surname) + "\t" + str('${:,.2f}'.format(self.cusLTVs[w]))
            data.append(str(datao))
            #print  str(self.customers.get(w).surname)  , w, self.cusLTVs[w]                    
        
        outputFile = conf.writeOutput(data)
        print 'OutPut File :' + outputFile
        return x 
        
#class CLTVTest(unittest.TestCase):
    

def main():
    if len(sys.argv) >= 3:
        topX = sys.argv[1]
        inFile = sys.argv[2]     
    else:
        print 'Please Enter Top X Customer & Input Data '
        inFile = 'D:\Projects\CLTV\input\ds50Customers.txt' 
        topX = 4 
     
    analysis = CLTV(inFile)
    analysis.TopXSimpleLTVCustomers(topX)
    
if __name__ == '__main__':
    main()   
    import doctest
    doctest.testmod()    
        
    