#!/usr/bin/env python3
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

class rPiScraper:
    def __init__(self,showItems=False,systemID=None,game=None):
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
        self.selectedText = None
        self.gameID = ''
        self.gameDict = {}
        self.sauce_ = None
        self.page_sauce_ = ''
        self.console_ = ''
        self.scrapeCache_ = 'scrapeCache'
        self.choices_ = ''
        self.systemGameDict = {}
        self.bs4Obj = ''
        SYSTEMS_fmt = {}
        for key,val in self.SYSTEMS_.items():
            SYSTEMS_fmt[val] = key
        self.SYSTEMS_ = SYSTEMS_fmt
        if showItems:
            pprint.pprint(self.SYSTEMS_)
        if systemID is None:
            try:
                systemID = int(input("Enter system ID#: ").strip())
            except Exception as e:
                print("Please enter a whole number that is a value in the list:\n\t" + str(e))
                sys.exit(-1)
                
        self.systemID = systemID
        self.url_ = "https://www.emuparadise.me/roms/gamebrowser.php?sort=name_Ascending&per_page=1000&gsysid%5B%5D={}&regions%5B%5D=Canada&regions%5B%5D=USA".format(self.systemID)
        self.rootUrl_ = "https://www.emuparadise.me"
        
        #-------------------------------------------------------------------------
    def makeRequest(self,game_url=None):
        '''Makes request to url and return status'''
        resetUrl = self.url_
        if game_url is not None:
            self.url_ = game_url
        try:
            print('You have selected {}'.format(self.SYSTEMS_[self.systemID]))
            print('Downloading page {}...'.format(self.url_))
        except Exception as e:
            print("TERMINATING PROGRAM due the following error:\n\t{}\n".format(e))
            sys.exit(-1)
        self.sauce_ = requests.get(self.url_)
        self.url_ = resetUrl
        return self.sauce_.status_code == requests.codes.ok
        
    def checkIfScraped(self,checkSysID=None):
        if self.systemID is not None:
            try:
                checkSysID = int(str(self.systemID).strip())
            except Exception as e:
                print("Bad input in method checkIfScraped: "+ str(e))
                sys.exit(-1)    
        if checkSysID is not None:
            try:
                checkSysID=int(str(checkSysID).strip())
            except Exception as e:
                print("Bad input in method checkIfScraped: "+ str(e))
                sys.exit(-1)
            try:
                system = os.path.join(self.scrapeCache_,self.SYSTEMS_[int(str(checkSysID).strip())]) + '.html'
                if os.path.exists(system):
                    return True
                else:
                    return False
            except Exception as e:
                print("TERMINATING PROGRAM: The following error has occured\n\t{}\n".format(e))
                return -1
        else:
            print('No entry has been made.')
            return -1
    
    def scrapeTopLevelPage(self):
        '''Scrapes entire page of selection'''
        if self.checkIfScraped(self.systemID):
            print('Locate games in: {}'.format(self.scrapeCache_))
        elif self.makeRequest():
            try:
                self.page_sauce_ = bs4.BeautifulSoup(self.sauce_.text,'lxml')
                if not os.path.isdir(self.scrapeCache_):
                    os.mkdir(self.scrapeCache_)
                with open(os.path.join(self.scrapeCache_,self.SYSTEMS_[self.systemID]+'.html'),'w') as systemGames:
                    systemGames.write(pprint.pformat(self.page_sauce_))
            except Exception as e:
                print("TERMINATING PROGRAM: The following error has occured\n\t{}\n".format(e))
                sys.exit(-1)
        
    def getGameDict(self,sysID=None):
        reGameDict = re.compile(r'=([0-9]{1,9})')
        gameDict = {}
        '''Make a dictionary of game names and game IDs for a console.'''
        if sysID is not None:
            self.systemID = int(str(sysID).strip())
        self.console = self.SYSTEMS_[self.systemID] + '.html'
        
        with open(os.path.join(self.scrapeCache_,self.console),'r') as consoleGames:
            bs4Obj = bs4.BeautifulSoup(consoleGames,'lxml')
        self.selectedText = bs4Obj.select('a[class="game-page-link"]')
        
        for tag in self.selectedText:
            tailRomlink = tag.attrs['href']
            name = tag.getText()
            romNumber = reGameDict.search(tailRomlink).group(1)
            gameDict[name] = [romNumber,tailRomlink]
        self.gameDict = gameDict
        #pprint.pprint(gameDict)
        return gameDict
    
    def searchRom(self,usrChoice): #string
        reSelect = re.compile(r'^[a-z0-9\s]{3,40}')
        partSelection = filter(lambda key: key.startswith(usrChoice.strip().title()),self.gameDict.keys())
        choices = {game:num for game,num in enumerate(partSelection,1)}
        if choices == {}:
            return False
        self.choices_ = choices
        pprint.pprint(choices)
        return choices
    
    def selectRom(self,enumNum):
        enumNum = int(enumNum)
        selectedGameUrl = self.gameDict[self.choices_[enumNum]][1]
        self.gameID = selectedGameUrl = self.gameDict[self.choices_[enumNum]][1]
        self.selection_ = self.choices_[enumNum]
        firstGameUrl = self.rootUrl_ + selectedGameUrl
        self.systemGameDict = {self.SYSTEMS_[self.systemID]:firstGameUrl}
        print(self.selection_,self.gameID)    
    
    # def downloadDirect(self,directID=None):
    #     thisDir = os.getcwd()
    #     if directID is not None:
    #         self.gameID = directID
    #     os.chdir('../')
    #     if not os.path.exists(os.path.join('Games')):
    #         os.mkdir('Games')
    #     if not os.path.exists(os.path.join('Games',self.selection_+'.zip')):
    #         downloadurl = self.rootUrl_+self.gameID
    #         print('Downloading page {}...'.format(downloadurl))
    #         self.sauce_ = requests.get(downloadurl)
    #         if not self.sauce_.status_code == 301:
    #             print(False)
    #     os.chdir(thisDir)
    #     return True
            
        
    def scrapeSecondLevelPage(self):
        #reGameDict = re.compile(r'=([0-9]{1,9})')
        val = self.systemGameDict[self.SYSTEMS_[self.systemID]]
        currentDir = os.getcwd()
        os.chdir('../')
        print(os.getcwd())
        if os.path.exists('gameScrape') is False:
            os.mkdir('gameScrape')
        if not os.path.exists(os.path.join('gameScrape',self.selection_+'.html')):
            self.makeRequest(val)
            self.page_sauce_ = bs4.BeautifulSoup(self.sauce_.text,'lxml')
        
            with open(os.path.join('gameScrape',self.selection_+'.html'),'w') as makesGamesHtml:
                makesGamesHtml.write(pprint.pformat(self.page_sauce_))
        
        with open(os.path.join('gameScrape',self.selection_+'.html'),'r') as gameScrapeTop:
            self.bs4Obj = bs4.BeautifulSoup(gameScrapeTop,'lxml')
            div = self.bs4Obj.find('div',{'class':'download-link'})
            a = div.find_all(href=True)[0]
            print(self.rootUrl_+a.attrs['href'])
        os.chdir(currentDir)
        #pprint.pprint(bs4Obj.getText())
        
        
        
if __name__ == "__main__":
    scrape = rPiScraper(showItems=True)
    scrape.scrapeTopLevelPage()
    scrape.getGameDict()
    choice = input("Enter game name: ")
    checkTrue = scrape.searchRom(choice)
    if not checkTrue:
        print('No Games with that name')
        sys.exit(-1)
    choice = input("Enter the number of the game: ")
    scrape.selectRom(choice)
    scrape.scrapeSecondLevelPage()
