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
    
    def test_content_testWeatherStationID(self):
        tester = create_app().test_client(self)

        response = tester.get("/Weather?StationID=test1")

        self.assertTrue(b'test1' in response.data)

    def test_content_testWeatherStationIDFail(self):
        tester = create_app().test_client(self)

        response = tester.get("/Weather?StationID=test2")

        self.assertFail(b'test2' in response.data)

    def test_content_testWeatherDate(self):
        tester = create_app().test_client(self)

        response = tester.get("/Weather?year=1993&month=06&date=11")

        self.assertTrue(b'test1' in response.data)
    
    def test_content_testWeatherDateFail(self):
        tester = create_app().test_client(self)

        response = tester.get("/Weather?year=1996&month=06&date=11")

        self.assertFail(b'test1' in response.data)

    def test_content_testWeatherAnalysis(self):
        tester = create_app().test_client(self)

        response = tester.get("/Weather/Stat?StationID=test1")

        self.assertTrue(b'test1' in response.data)
    
    def test_content_testWeatherAnalysisFail(self):
        tester = create_app().test_client(self)

        response = tester.get("/Weather/Stat?StationID=test2")

        self.assertTrue(b'test2' in response.data)

    def test_content_testWeatherDateAnalysisDate(self):
        tester = create_app().test_client(self)

        response = tester.get("/Weather/Stat?year=1993")

        self.assertTrue(b'test1' in response.data)

    def test_content_testWeatherDateAnalysisDateFail(self):
        tester = create_app().test_client(self)

        response = tester.get("/Weather/Stat?year=1693")

        self.assertFail(b'test1' in response.data)

if __name__ == "__main__":
    unittest.main()