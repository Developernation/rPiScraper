import bs4
import webbrowser
import requests
import logging
import os
import argparse
import pprint
import sys
import re

logging.basicConfig(level = logging.DEBUG, format = ' %(asctime)s - %(levelname)s - %(message)s')
logging.debug('Start of program')

class reFactorScraper:
    def __init__(self,systemID,showItems=False,game=None):
        self.SYSTEMS_ = {
        'Abandonware': 51, 'Acorn Archimedes': 58, 'Acorn BBC Micro': 59, 'Acorn Electron': 60,
        'Amiga': 4, 'Amiga CD': 52, 'Amiga CD32': 22, 'Amstrad CPC': 62, 'Android': 65,
        'Apple ][': 24, 'Atari 2600': 49, 'Atari 5200': 48, 'Atari 7800': 47, 'Atari 8-bit Family': 57,
        'Atari Jaguar': 50, 'Atari Lynx': 28, 'Atari ST': 63, 'Bandai Playdia': 56, 'Bandai Wonderswan': 39,
        'Bandai Wonderswan Color': 40, 'Capcom Play System 1': 54, 'Capcom Play System 2': 55,
        'Capcom Play System 3': 66, 'Commodore 64 (Tapes)': 34, 'Commodore 64 Preservation Project': 33,
        'Complete ROM Sets (Full Sets in One File)': 37, 'iPod Touch - iPhone': 45,
        'M.A.M.E. - Multiple Arcade Machine Emulator': 7, 'Microsoft XBox': 43, 'Miscellaneous': 46,
        'Neo Geo': 26, 'Neo Geo Pocket - Neo Geo Pocket Color (NGPx)': 38, 'Neo-Geo CD': 8,
        'Nintendo 64': 9, 'Nintendo DS': 32, 'Nintendo Entertainment System': 13,
        'Nintendo Famicom Disk System': 29, 'Nintendo Game Boy': 12, 'Nintendo Game Boy Color': 11,
        'Nintendo Gameboy Advance': 31, 'Nintendo Gamecube': 42, 'Nintendo Virtual Boy': 27,
        'Nintendo Wii': 68, 'Nokia N-Gage': 17, 'Panasonic 3DO (3DO Interactive Multiplayer)': 20,
        'PC Engine - TurboGrafx16': 16, 'PC Engine CD - Turbo Duo - TurboGrafx CD': 18, 'PC-FX': 64,
        'Philips CD-i': 19, 'PSP': 44, 'PSX on PSP': 67, 'ScummVM': 21, 'Sega 32X': 61, 'Sega CD': 10,
        'Sega Dreamcast': 1, 'Sega Game Gear': 14, 'Sega Genesis - Sega Megadrive': 6, 'Sega Master System': 15,
        'Sega NAOMI': 30, 'Sega Saturn': 3, 'Sharp X68000': 23, 'Sony Playstation': 2, 'Sony Playstation 2': 41,
        'Sony Playstation - Demos': 25, 'Sony Playstation - Old': 1069, 'Sony PocketStation': 53,
        'Super Nintendo Entertainment System (SNES)': 5, 'ZX Spectrum (Tapes)': 36, 'ZX Spectrum (Z80)': 35
        }
        self.systemID = systemID
        self.SystemNums_ = {val:key for key,val in self.SYSTEMS_.items()} 
        self.system = ""
        self.selectedText = [] 
        self.choices_ = {}
            
        self.rootUrl_ = "https://www.emuparadise.me"
        self.gameBrowserAddon = "/roms/gamebrowser.php?sort=name_Ascending&per_page=1000&gsysid%5B%5D={}&regions%5B%5D=Canada&regions%5B%5D=USA".format(self.systemID)
        self.url2scrape = ""
        
    def setValidSysNum(self):
        '''sets the system number'''
        if self.systemID in self.SystemNums_:
            self.system = self.SystemNums_[self.systemID]
            return True
        return False
    
    def checkIfScraped(self):
        return os.path.exists(os.path.join('scrapeCache',self.system + '.html'))
    
    def getSystemGames(self):
        with open(os.path.join('scrapeCache',self.system + '.html'),'r') as consoleGames:
            bs4Obj = bs4.BeautifulSoup(consoleGames,'lxml')
        self.selectedText =[item for item in bs4Obj.select('a[class="game-page-link"]')]
        return len(self.selectedText)
    
    def makeGameDict(self):
        reGameDict = re.compile(r'=([0-9]{1,9})')
        gameDict = {}
        for tag in self.selectedText:
            tailRomlink = tag.attrs['href']
            name = tag.getText()
            romNumber = reGameDict.search(tailRomlink).group(1)
            gameDict[name] = [romNumber,tailRomlink]
        self.gameDict = gameDict
        return len(self.gameDict.keys())
    
    def gameSelector(self,usrChoice):
        '''Allows the user to select a game from the enumerated dict of choices'''
        reSelect = re.compile(r'^[a-z0-9\s]{3,40}')
        partSelection = filter(lambda key: key.startswith(usrChoice.strip().title()),self.gameDict.keys())
        choices = {game:num for game,num in enumerate(partSelection,1)}
        if choices == {}:
            return -1
        self.choices_ = choices
        pprint.pprint(choices)
        return len(choices)
    
    def makeChoice(self):
        '''pick a game from the list of choices'''
        return 0
    
    def urlBuilder(self,scrapeSystems=False):
        if scrapeSystems:
            return self.rootUrl_ + self.gameBrowserAddon
        
        
    def makeScrape(self):
        return 0
        # self.url2scrape = 
        # print('You have selected {}'.format(self.system))
        # print('Downloading page {}...'.format(self.url_)) 
    
    def maybeScrape(self):
        if self.checkIfScraped():
            return "Already scraped, proceeding to analyze."
        else:
            self.makeScrape()
    
        
        

        
    
    # def makeRequest(self,url):
    #     '''Makes request to url and return status'''
    #     try:
    #         print('You have selected {}'.format(self.SYSTEMS_[self.systemID]))
    #         print('Downloading page {}...'.format(self.url_))
    #     except Exception as e:
    #         print("TERMINATING PROGRAM due the following error:\n\t{}\n".format(e))
    #         sys.exit(-1)
    #     self.sauce_ = requests.get(self.url_)
    #     self.url_ = resetUrl
    #     return self.sauce_.status_code == requests.codes.ok