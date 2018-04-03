import unittest 
from rPiScraper import rPiScraper


class Test_rPiScraper(unittest.TestCase):
    
    def test_makeRequest(self):
        scraper_obj = rPiScraper(5)
        
        response = scraper_obj.makeRequest()
        
        self.assertTrue(response)
        
        