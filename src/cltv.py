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
        
        
    def loadJson(self, fileName):
        
        if fileName:
            with open(fileName, 'r') as f:
                objects = json.load(f)
            if len(objects)>1:
                for event in objects:
                    self.ingest(event) 
        else:
            return None
        
    def ingest(self, data):
        event = Event(data)
        eType   = event.eType
        eAction = event.eAction 
        eTime   = event.eTime 
        eYear   = event.eYear 
        eWeek   = event.eWeek 
        eYWeek  = event.eYWeek  # 99-00 bad weekly data 
        
        if eType == 'CUSTOMER':
            if data.get('key') in self.customers:
                #self.customers.get(data.get('key')).update(customer)
                x =0  
            else:
                customer = Customer(data)
                self.customers[data.get('key')] = customer
        #print self.customers        
        if eType == 'SITE_VISIT':
            customer_id = data.get('customer_id')
            if customer_id not in self.customers:
                customer = Customer(data)
                self.customers[customer_id] = customer
            self.customers.get(customer_id).cntVisit += 1
                
            if self.customers.get(customer_id , {}).wkVisits.get(eYWeek) :
                self.customers.get(customer_id).wkVisits[eYWeek]  += 1
            else:
                wklVists =1
                self.customers.get(customer_id).wkVisits[eYWeek]  = wklVists
        if eType == 'ORDER':
            customer_id = data.get('customer_id')
            s = data.get('total_amount')
            expen = Decimal(re.sub("[^0-9|.]", "", s))  # 123456.79
            if customer_id not in self.customers:
                customer = Customer(data)
                self.customers[customer_id] = customer 
            self.customers.get(customer_id).totExpend += expen     
            if self.customers.get(customer_id , {}).wkExpend.get(eYWeek) :
                self.customers.get(customer_id).wkExpend[eYWeek]  += expen
            else:
                self.customers.get(customer_id ).wkExpend[eYWeek]  = expen
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
        
    def TopXSimpleLTVCustomers(self,x):
       #outputFile = conf.set_outFile('outpu')
        conf = Config()
        data = []
        topX = int(x)
        
            #conf.writeOutput(sorted(self.cusLTVs, key=self.cusLTVs.get, reverse=True)[:topX])
        for w in sorted(self.cusLTVs, key=self.cusLTVs.get, reverse=True)[:x]:
            datao = str(w) + "\t"+ str(self.customers.get(w).last_name) + "\t" + str('${:,.2f}'.format(self.cusLTVs[w]))
            data.append(str(datao))
            print  str(self.customers.get(w).last_name)  , w, self.cusLTVs[w]                    
        
        outputFile = conf.writeOutput(data)
        print outputFile
        return x 
        
#class CLTVTest(unittest.TestCase):
    

def main():
    if len(sys.argv) >= 3:
        topX = sys.argv[1]
        inFile = sys.argv[2]     
    else:
        print 'Please Enter Top X Customer & Input Data '
        return 
     
    analysis = CLTV(inFile)
    analysis.TopXSimpleLTVCustomers(topX)
    
if __name__ == '__main__':
    main()   
    import doctest
    doctest.testmod()    
        
    