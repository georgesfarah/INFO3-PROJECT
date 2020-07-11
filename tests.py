import unittest 

from Model import FetchData
from Model import create_connection
from Model import select_by_country
from Model import Location
from Model import hashpasswordInit

import pickle

class MyTests(unittest.TestCase):
    

    def test_StoretoDB(self):
        a=FetchData()
        self.assertTrue(a)

    def test_DataCorrect1(self):
        conn=create_connection()
        data=select_by_country(conn,'ASC')
        conn.close()
        #id countryName deaths confirmed recovered lastchecked
        countryNameTrue='France'
        deaths=24760
        confirmed=168396
        recovered=50562
        
        for elm in data:
            if elm[1]==countryNameTrue:
                self.assertEqual(elm[2],deaths)
                self.assertEqual(elm[3],confirmed)
                self.assertEqual(elm[4],recovered)


    def testConfigsExists(self):
        f=open('configs.txt','rb')
        data=pickle.load(f)
        f.close()

        self.assertTrue('fontSize' in data.keys())
        self.assertTrue('color' in data.keys())

    def test_Location(self):
      a=Location.getLocation()
      self.assertTrue(a)

    def test_hashing(self):
        a=hashpasswordInit('test')['key']
        b="b'\\xfb\\xb7\\xa6^\\x83\\x86\\x04\\x03Qp\\xe7,Q\\x07\\xdec\\xf7J&\\xf0Y\\x13\\x18\\xa2O\\xf7#\\xa7\\xd5\\x03B>'"
        self.assertEqual(a,b)
        

if __name__ == '__main__': 
    unittest.main()
