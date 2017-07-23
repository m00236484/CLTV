import ijson
import pandas as pd
from datetime import datetime

filename = 'input.txt'
customers = {}
with open(filename, 'r') as f:
    objects = ijson.items(f, '')
    columns = list(objects)
    for column in columns:
        for items in column:
            if items['type'] == 'CUSTOMER':
                customerId =  str(items['key'])
                if customerId not in customers:
                    eTime = datetime.strptime(items['event_time'], '%Y-%m-%dT%H:%M:%S.%fZ')
                    year = eTime.year
                    wkNumber = eTime.isocalendar()[1]                    
                    customers[customerId] = {year:{wkNumber:[ 0 , 0]}}
                    #print customers
            elif items['type'] == 'SITE_VISIT':
                customerId =  str(items['customer_id'])
                eTime = datetime.strptime(items['event_time'], '%Y-%m-%dT%H:%M:%S.%fZ')
                year = eTime.year
                wkNumber = eTime.isocalendar()[1]
                
                if customerId  in customers:
                    print 2
                    cusYear = customers.get(customerId)
                    if year in cusYear:
                        print 3
                        cusWeek = cusYear.get(year)
                        print cusWeek , wkNumber 
                        if wkNumber in cusWeek:
                            
                            custVal = cusWeek.get(wkNumber)
                            custVal[1] = custVal[1]  + 1
                            print custVal
                
                    
                      
                    
                
            '''    
                print items['key']
            elif items['type'] == 'ORDER':
                print items['key']
            elif items['type'] == 'IMAGE':
                print items['key']
            '''    
        
        
    #print(columns) 
