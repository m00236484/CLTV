import unittest
from cltv import CLTV
import sys
class CLTVTestCase(unittest.TestCase):
   
    def setUp(self):
        fileName = 'D:\Projects\CLTV\input\ds50Customers.txt'
        #fileName = 'D:\Projects\CLTV\input\input.txt'         
        self.cltv = CLTV(fileName)

    def test_TopXSimpleLTVCustomers(self, topX):      
        try:
            self.assertEquals(self.cltv.TopXSimpleLTVCustomers(topX),topX, msg='Return Lesss' )
        except Exception, e:
            msg = str(e)
            shortened_msg = (msg[:100]+'...' if len(msg)>100 else msg)
            raise self.failureException(shortened_msg)        
            
if __name__ == '__main__':

    
    
    unittest.main()