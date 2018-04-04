import unittest 
from reFactorScraper import reFactorScraper
#from reFactorScraper import validSysNum


class test_reFactorScraper(unittest.TestCase):
    
    def test_setValidSysNum(self):
        scraper = reFactorScraper(5)
            
        testBool = scraper.setValidSysNum()
        
        self.assertTrue(testBool)
    
    def test_checkIfScraped(self):
        scraper2 = reFactorScraper(5)
        
        scraper2.setValidSysNum()

        self.assertTrue(scraper2.checkIfScraped())
    
    def test_getSystemGames(self):
        scraper3 = reFactorScraper(5)
        
        scraper3.setValidSysNum()

        scraper3.checkIfScraped()
        
        self.assertTrue(scraper3.getSystemGames() > 0)
    
    def test_maybeScrape(self):
        scraper4 = reFactorScraper(5)
        
        scraper4.setValidSysNum()

        scraper4.checkIfScraped()
        
        scraper4.getSystemGames()
        
        self.assertEqual(scraper4.maybeScrape(),"Already scraped, proceeding to analyze.")
        
    def test_makeGameDict(self):
        scraper5 = reFactorScraper(5)
        
        scraper5.setValidSysNum()

        scraper5.checkIfScraped()
        
        scraper5.getSystemGames()
        
        scraper5.makeGameDict()
        
        self.assertTrue(scraper5.makeGameDict() == scraper5.getSystemGames())
    
    def test_urlBuilder(self):
        
        scraper6 = reFactorScraper(5)
        
        scraper6.setValidSysNum()

        scraper6.checkIfScraped()
        
        scraper6.getSystemGames()
        
        scraper6.makeGameDict()
        
        self.assertEqual(scraper6.urlBuilder(True),"https://www.emuparadise.me"+"/roms/gamebrowser.php?sort=name_Ascending&per_page=1000&gsysid%5B%5D={}&regions%5B%5D=Canada&regions%5B%5D=USA".format(5))
    
    def test_gameSelector(self):
        scraper7 = reFactorScraper(5)
        
        scraper7.setValidSysNum()

        scraper7.checkIfScraped()
        
        scraper7.getSystemGames()
        
        scraper7.makeGameDict()
        
        num = scraper7.gameSelector('re')
        
        self.assertTrue(num != -1)   
        
        
    
    # def test_makeScrape(self):
    #     scraper5 = reFactorScraper(5)
        
    #     scraper5.setValidSysNum()

    #     scraper5.checkIfScraped()
        
    #     scraper5.getSystemGames()
        
    #     scraper5.maybeScrape()
        
    #     self.assertTrue(scraper5.makeScrape())

        
        
        
if __name__ == '__main__':
    unittest.main()