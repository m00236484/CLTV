
class Customer(object):
    
    def __init__(self, data):
        self.data = data 
        self.key = self.data.get('key')
        self.last_name = self.data.get('last_name')
        self.cntVisit  = 0
        self.totExpend = 0
        self.visExpend = 0
        self.cusValue  = 0
        self.wkVisits = dict()
        self.wkExpend = dict()
        
    def set_cntVisit(self):
        self.cntVisit += 1
        
    def set_totExpend(self, amount):
        self.totExpend += amount
        
