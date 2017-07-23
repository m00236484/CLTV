import ijson
import pandas as pd
from datetime import datetime
from decimal import Decimal
import re
import pandas as pd

def readJson(filename):
    customers = []
    customer = [] # CustomerId,Year,weekNo,visits#,expense
    with open(filename, 'r') as f:
        objects = ijson.items(f, '')
        columns = list(objects)
        for column in columns:
            for items in column:
                customer = []
                if items['type'] == 'CUSTOMER':
                    customerId =  str(items['key'])
                    
                    eTime = datetime.strptime(items['event_time'], '%Y-%m-%dT%H:%M:%S.%fZ')
                    year = eTime.year
                    wkNumber = eTime.isocalendar()[1]
                    customer.append(customerId)
                    customer.append(year)
                    customer.append(wkNumber)
                    customer.append(0)
                    customer.append(0)
                    customers.append(customer)                
                    
                elif items['type'] == 'SITE_VISIT':
                    customerId =  str(items['customer_id'])
                    eTime = datetime.strptime(items['event_time'], '%Y-%m-%dT%H:%M:%S.%fZ')
                    year = eTime.year
                    wkNumber = eTime.isocalendar()[1]
                    customer.append(customerId)
                    customer.append(year)
                    customer.append(wkNumber)
                    customer.append(1)
                    customer.append(0)
                    customers.append(customer)
                    
                elif items['type'] == 'ORDER':
                    customerId =  str(items['customer_id'])
                    eTime = datetime.strptime(items['event_time'], '%Y-%m-%dT%H:%M:%S.%fZ')
                    year = eTime.year
                    wkNumber = eTime.isocalendar()[1]
                    s = str(items['total_amount'])
                    expen = Decimal(re.sub("[^0-9|.]", "", s))  # 123456.79
                    customer.append(customerId)
                    customer.append(year)
                    customer.append(wkNumber)
                    customer.append(0)
                    customer.append(expen)
                    customers.append(customer)                              
                          
                        
        return customers           
def processingDF(customers):
    columns = ['customer', 'year','wkNumber','vistNo','wkTot']
    table = pd.DataFrame(customers, columns=columns)
    df2=table.groupby(['customer', 'year','wkNumber']).agg({"wkTot": "sum","vistNo":"count"})
    customerCount = table.groupby('customer').nunique()
    print (df2)
    #print (customerCount)

    
    
     
    
def main():
    filename = 'input.txt'
    customers = readJson(filename)
    processingDF(customers)
    #print(len(customers))
    
if __name__ == '__main__':
    main()     
    #print(columns) 
