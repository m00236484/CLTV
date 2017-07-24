import sys
import os
import json
import unittest
import math
import operator
from decimal import Decimal
import re
from customer import Customer
from event import Event
from config import Config

class CLTV(object):
     
    def __init__(self, fileName):
        self.conf = Config()
        self.event = Event()
        
        self.customers = {}
        self.cusLTVs = {}
        self.cusLTVsDF ={}
        self.VisitsNo = 0
        self.ordersNo = 0
        self.badEvent = 0
        self.events = 0 
        self.inFile = fileName
        self.outFile = ''
        self.logFile = ''
        self.badDataFile = ''
        self.dsFile = ''
        self.set_OutputFiles()
        
        # set log file to event 
        self.event.badEventFile =  self.badDataFile
        
        self.avrcusLTV = 0     
        self.avrWkVisit  = 0 
        self.avrVistExpe = 0 
        self.avrWklyExpe = 0 
        
        self.avrcusLTVTF = 0     
        self.avrWkVisitTF  = 0 
        self.avrVistExpeTF = 0 
        self.avrWklyExpeTF = 0 
        
        if self.loadJson(fileName):
                 
            self.analysis()
            self.analysis_dateFrame()
            self.dataSet_analsys()
            
    def set_OutputFiles(self):
          
        self.outFile =  self.conf.set_outFile('output')   
        self.logFile =  self.conf.set_outFile('log')   
        self.badDataFile = self.conf.set_outFile('badFile')   
        self.dsFile = self.conf.set_outFile('DS_Analsis')        
        
        
    def loadJson(self, fileName):
        
        if os.path.isfile(fileName): 
            with open(fileName, 'r') as f:
                try:
                    objects = json.load(f)
                    
                    if len(objects)>=1:   
                        for event in objects:
                            self.ingest(event)
                    else:
                        self.conf.writeOutput(self.logFile , 'Input file is empty ###: ' + fileName , True )
                        return False
                    
                except ValueError, e:
                    print e.message  
                    self.conf.writeOutput(self.logFile , 'Input file is empty ***  : ' + fileName , True )
                    return False
                                                      
        else:
            self.conf.writeOutput(self.logFile , 'Input file dose not exists : ' + fileName , True )
            return False
          
        self.conf.writeOutput(self.logFile , 'Success to read json file : ' + fileName , True )
        return True
    def ingest(self, event):

        data = self.event.getEventData(event)
        self.events += 1
        if not data:
            self.badEvent += 1
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
                    self.VisitsNo += 1               
                elif eType == 'ORDER':
                    expen = data.get('total_amount')
                    self.customers.get(customer_id).set_customerVisit(eTime, eYWeek , expen )
                    self.ordersNo += 1 
              


    def analysis(self):
        vistExpe = 0
        wkVisit = 0
        cusCount = len(self.customers.keys())
           
        for key  in self.customers:
            #print self.customers.get(key).totExpend
            try:
                cusVstExpe = self.customers.get(key).totExpend / self.customers.get(key).cntVisit
            except:
                cusVstExpe = 0 
                
            vistExpe += cusVstExpe
            try:
                cusVstWklV = self.customers.get(key).cntVisit / len(self.customers.get(key).wkVisits.keys())
            except:    
                cusVstWklV = 0
            wkVisit += cusVstWklV    
            wkCustVal = cusVstExpe * cusVstWklV
            cusLTV = 52 * wkCustVal * 10
            self.cusLTVs[key] = cusLTV
            self.cusLTVs['cusVstExpe'] = cusVstExpe
            self.cusLTVs['cusVstWklV'] = cusVstWklV            
        try:
            avrVistExpe  = vistExpe /  cusCount
        except:    
            avrVistExpe = 0 
        try:
            avrWkVisit   = wkVisit / cusCount
            
        except:    
            avrWkVisit = 0        
        
        avrcusLTV    = 52 * (avrVistExpe * avrWkVisit) * 10 
        
        self.avrcusLTV =avrcusLTV     
        self.avrWkVisit  = avrWkVisit 
        self.avrVistExpe =avrVistExpe 
        self.avrWklyExpe = avrVistExpe * avrWkVisit 
    
              
    
    def dataSet_analsys(self):
        data = []
        event =     'Total Events      :' + str(self.events) 
        client =    'Total Clients     :' + str(len(self.customers.keys()))
        Visits =    'Total Visits      :' + str(self.VisitsNo)
        Orders =    'Total Orders      :' + str(self.ordersNo)
        bad_event = 'Total Bad Events  :' + str(self.badEvent)
        data.append(event)
        data.append(client)
        data.append(Visits)
        data.append(Orders)
        data.append(bad_event)  
        outputFile = self.conf.writeOutput(self.dsFile , data)
        
    def analysis_dateFrame(self):
        vistExpe = 0
        wkVisit = 0
        cusCount = len(self.customers.keys())
        for key  in self.customers:
            #print self.customers.get(key).totExpend
            try:
                cusVstExpe = self.customers.get(key).totExpend / self.customers.get(key).cntVisit
            except:    
                cusVstExpe = 0
            vistExpe += cusVstExpe 
            
            firstAction = self.customers.get(key).firstAction 
            lastAction =  self.customers.get(key).lastAction
            
            try:
                Weeks = (lastAction-firstAction).days / 7
                weeks = math.ceil(Weeks)
            except:    
                Weeks = 1  
            
            try:
                cusVstWklV = self.customers.get(key).cntVisit / Weeks
                cusVstWklV = math.ceil(cusVstWklV)
            except:    
                cusVstWklV = 0 
            #print  math.ceil(cusVstWklV) , '\t', cusVstWklV
            wkVisit += cusVstWklV  
            wkCustVal = Decimal(cusVstExpe) * Decimal(cusVstWklV)
        
            cusLTV = 52 * wkCustVal * 10
          
            self.customers.get(key).set_custValue(cusLTV, cusVstExpe , cusVstWklV )
            
            

        try:
            avrVistExpe  = vistExpe /  cusCount
        except:    
            avrVistExpe = 0 
        try:
            avrWkVisit   = round(wkVisit / cusCount)
        except:    
            avrWkVisit = 0
     
            
        avrWklyExpeTF  = Decimal(avrVistExpe) * Decimal(avrWkVisit)
        avrcusLTV    = 52 * avrWklyExpeTF * 10 
       
        
        self.avrcusLTVTF = avrcusLTV     
        self.avrWkVisitTF  = avrWkVisit 
        self.avrVistExpeTF = avrVistExpe 
        self.avrWklyExpeTF = Decimal(avrVistExpe) * Decimal(avrWkVisit)  
        
    def custSegmentation(self):
        avrCLTV = self.avrcusLTVTF
        oldSeg = ''
        newSeg = ''
        cnt = 0 
        flag = False 
        customerCnt = len(self.customers.keys())
        self.conf.writeOutput(self.outFile ,'\n'+'--------------------------------------------------------------------------------------') 
        self.conf.writeOutput(self.outFile ,'C-' +'\t' +'Customer Segmentation Based on Customer Lifetime Value ' + '\n')
        
        self.conf.writeOutput(self.outFile ,'  ID ' + '\t' + 'Name' + '\t' + 'Customer Segment' +'\n')
        
        for customer in (sorted(self.customers.values(), key=operator.attrgetter('cusLTV'), reverse=True)):
            cusval =  round(((customer.cusLTV / avrCLTV) * 100 ))
            if  cusval > 130 :
                newSeg = 'A'
                self.customers.get(customer.key).set_custSegment('A')
            elif  cusval >= 105 and cusval < 130 : 
                newSeg = 'B'
                self.customers.get(customer.key).set_custSegment('B')
            elif  cusval >= 90 and cusval < 105 : 
                newSeg = 'C'
                self.customers.get(customer.key).set_custSegment('C')                
            elif  cusval >= 80 and cusval < 90 : 
                newSeg = 'D'
                self.customers.get(customer.key).set_custSegment('D')                
            else:
                newSeg = 'E'
                self.customers.get(customer.key).set_custSegment('E')                
            
            if oldSeg == newSeg:
                cnt +=1
                self.conf.writeOutput(self.outFile ,str(customer.key) + '\t' + str(customer.surname) + '\t' + str(customer.segment))
            else:
  
                try:
                    
                    prec = math.ceil( (cnt * 100 ) / customerCnt)  

                except:
                    prec = 0
                #print prec 
                if flag:
                    self.conf.writeOutput(self.outFile ,'Total Customer in  Segment  ' + oldSeg + ' Is  : ' + str(cnt) + '   Precentage : ' +str('{:}%'.format(prec))  )
                self.conf.writeOutput(self.outFile ,'\n'+'------------------ Segment '+ newSeg +'  ----------------------')                 
                self.conf.writeOutput(self.outFile ,str(customer.key) + '\t' + str(customer.surname) + '\t' + str(customer.segment))
                cnt = 0
                flag = True 
                oldSeg = newSeg
            
    def TopXSimpleLTVCustomers(self,x):
       #outputFile = conf.set_outFile('outpu')
        
        data = []
        topX = 0
        
        self.cusLTVsDF
        customerCNT = len(self.customers.keys())
        self.conf.writeOutput(self.outFile ,'A-' +'\t' +'Calculate Topx Customer Lifetime Value Timeframe')
        self.conf.writeOutput(self.outFile ,'Total Count OF Clients               :' + str(customerCNT) )
        self.conf.writeOutput(self.outFile ,'Averge Customers CLTV                :' + str('${:,.2f}'.format(self.avrcusLTVTF )) )
        self.conf.writeOutput(self.outFile ,'Averge Customers Weekly Visit        :' + str('{:}'.format(self.avrWkVisitTF )) )
        self.conf.writeOutput(self.outFile ,'Averge Customers Visit  Expenditure  :' + str('${:,.2f}'.format(self.avrVistExpeTF )) )
        self.conf.writeOutput(self.outFile ,'Averge Customers Weekly Expenditure  :' + str('${:,.2f}'.format(self.avrWklyExpeTF )) + '\n')
        
    
  
        
        if int(x) <= customerCNT:
            topX = x
        else:
            topX = customerCNT
       
        #for w in (sorted(self.customers.values(), key=operator.attrgetter('cusLTV'), reverse=True)):
        #    print w.key , w.cusLTV
  
        count = 1
        self.conf.writeOutput(self.outFile ,'  ID ' + '\t' + 'Name' + '\t' +  'Expendure Vist'+ '\t'+'Weekly Visit'+ '\t'  + 'Customer CLTV')
        for x in (sorted(self.customers.values(), key=operator.attrgetter('cusLTV'), reverse=True)):
            w = x.key 
            cusLTVsDF =self.customers.get(w).cusLTV
            wkVst     =self.customers.get(w).wkVst
            vstExpend     =self.customers.get(w).vstExpend
            
            datao = str(w) + "\t"+ str(self.customers.get(w).surname) + "\t" +str( '${:,.2f}'.format(vstExpend) )+'\t'+str(wkVst)+ '\t'+ str('${:,.2f}'.format(cusLTVsDF))
            data.append(str(datao))
            #print  str(self.customers.get(w).surname)  , w, self.cusLTVs[w]
            if int(topX) == count:
                break
            else:
                count += 1 
            
        outputFile = self.conf.writeOutput(self.outFile ,data)
        
        data = []
        self.conf.writeOutput(self.outFile ,'--------------------------------------------------------------------------------------')    
        self.conf.writeOutput(self.outFile , '\n' + '\n' +'B-' +'\t'+'Calculate Topx Customer Live Time Value Based on numbers of weeks that user already visited')
        self.conf.writeOutput(self.outFile ,'Total Count OF Clients  :' + str(customerCNT))    
        self.conf.writeOutput(self.outFile ,'Averge Customers CLTV                :' + str('${:,.2f}'.format(self.avrcusLTV )) )
        self.conf.writeOutput(self.outFile ,'Averge Customers Weekly Visit        :' + str('{:}'.format(self.avrWkVisit )) )
        self.conf.writeOutput(self.outFile ,'Averge Customers Visit  Expenditure  :' + str('${:,.2f}'.format(self.avrVistExpe )) )
        self.conf.writeOutput(self.outFile ,'Averge Customers Weekly Expenditure  :' + str('${:,.2f}'.format(self.avrWklyExpe )) + '\n')
        
        self.conf.writeOutput(self.outFile , '\n'+'  ID ' + '\t' + 'Name' + '\t' +  'Expendure Vist'+ '\t'+'Weekly Visit'+ '\t'  + 'Customer CLTV') 
        for w in sorted(self.cusLTVs, key=self.cusLTVs.get, reverse=True)[:int(topX)]:
            datao = str(w) + "\t"+ str(self.customers.get(w).surname) + "\t" +str( '${:,.2f}'.format(self.cusLTVs['cusVstExpe']) )+'\t'+str(self.cusLTVs['cusVstWklV'] )+ '\t'+ str('${:,.2f}'.format(self.cusLTVs[w]))
            
            data.append(str(datao))
            #print  str(self.customers.get(w).surname)  , w, self.cusLTVs[w]                    
        
             
        outputFile = self.conf.writeOutput(self.outFile ,data)
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
    if len(analysis.customers.keys()) > 1:
        
        analysis.TopXSimpleLTVCustomers(topX)
        analysis.custSegmentation()
    
if __name__ == '__main__':
    main()   
    import doctest
    doctest.testmod()    
        
    