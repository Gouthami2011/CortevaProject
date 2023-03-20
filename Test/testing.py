import unittest
from main import *
from app import create_app
import logging

logging.basicConfig(filename='std.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')

#Let us Create an object 
log=logging.getLogger() 

class AppTestCase(unittest.TestCase):
    def setUp(self):

        performETL(log, test="test")

    def test_index_content(self):
        tester = create_app().test_client(self)

        response = tester.get("/Weather")
        self.assertEqual(response.content_type, "application/json")
    
    def test_content_testWeather(self):
        tester = create_app().test_client(self)

        response = tester.get("/Weather?StationID=test1")

        self.assertTrue(b'test1' in response.data)

    def test_content_testWeatherAnalysis(self):
        tester = create_app().test_client(self)

        response = tester.get("/Weather/Stat?StationID=test1")

        self.assertTrue(b'test1' in response.data)

if __name__ == "__main__":
    unittest.main()