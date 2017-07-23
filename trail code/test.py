import ijson
import pandas as pd
from datetime import datetime
from decimal import Decimal
import re

filename = 'input.txt'
customers = {}
with open(filename, 'r') as f:
    objects = ijson.items(f, '')
    columns = list(objects)
    for column in columns:
        for items in column:
            if items['type'] == 'CUSTOMER':
                customerId =  str(items['key'])
                eTime = datetime.strptime(items['event_time'], '%Y-%m-%dT%H:%M:%S.%fZ')
                year = eTime.year
                wkNumber = eTime.isocalendar()[1]
                customerKey = customerId + '-'+str(year)+'-' + str(wkNumber)
                if customerKey not in customers:
                    customers[customerKey] = [0,0]                    
                    
            elif items['type'] == 'SITE_VISIT':
                customerId =  str(items['customer_id'])
                eTime = datetime.strptime(items['event_time'], '%Y-%m-%dT%H:%M:%S.%fZ')
                year = eTime.year
                wkNumber = eTime.isocalendar()[1]
                customerKey = customerId + '-'+str(year)+'-' + str(wkNumber)
                if customerKey  in customers:
                    customers[customerKey][0] += 1                  
            elif items['type'] == 'ORDER':
                customerId =  str(items['customer_id'])
                eTime = datetime.strptime(items['event_time'], '%Y-%m-%dT%H:%M:%S.%fZ')
                year = eTime.year
                wkNumber = eTime.isocalendar()[1]
                s = str(items['customer_id'])
                expen = Decimal(re.sub("[^0-9|.]", "", s))   # 123456.79
                customerKey = customerId + '-'+str(year)+'-' + str(wkNumber)
                if customerKey  in customers:
                    customers[customerKey][1] += expen              
                      
            print customers         
                
            '''    
                print items['key']
            elif items['type'] == 'ORDER':
                print items['key']
            elif items['type'] == 'IMAGE':
                print items['key']
            '''    
        
        
    #print(columns) 
