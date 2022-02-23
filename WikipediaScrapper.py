from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as bs
from utils import beautifyLinkData, beautifyImgdata, summarize
from logger import getLog

logger=getLog('Scrapper.py')


class Scrapper():

    def __init__(self,searchString):

        try:
            self.searchString = str(searchString)
            self.url="https://en.wikipedia.org/wiki/"+self.searchString
            logger.info("Scrapper object initialized")
        except Exception as e:
            logger.exception(f'Something went wrong while Initialising Scrapper Object :\n{str(e)}')

    def getContent(self):

        try:
            uClient = uReq(self.url)
            Page = uClient.read()
            uClient.close()
            html = bs(Page, "html.parser")
            logger.info("URL hitted")
            return html
        except Exception as e:
            logger.exception(f'Something went wrong while Hitting the Page : \n {str(e)}')

    def getTextdata(self,html):

        try:
            info=html.find('div',{'class':"mw-body-content mw-content-ltr"}).find_all('p')
            logger.info("Text raw data retrieved")
            return summarize(info)
        except Exception as e:
            logger.exception(f'Something went wrong while fetching Text Data :\n{str(e)}')

    def getReference(self,html):

        try:
            info=html.find('div',{'class':"mw-body-content mw-content-ltr"}).find_all('a',href=True)
            logger.info('Reference raw data retrieved')
            return beautifyLinkData(info,self.searchString)
        except Exception as e:
            logger.exception(f'Something went wrong while fetching Reference Links :\n{str(e)}')

    def getImages(self,html):
        
        try:
            info=html.find('div',{'class':"mw-body-content mw-content-ltr"}).find_all('img')
            logger.info("Image Raw data retrieved")
            return beautifyImgdata(info)
        except Exception as e:
            logger.exception(f'Something went wrong while fetching Image Data :\n{str(e)}')

        
