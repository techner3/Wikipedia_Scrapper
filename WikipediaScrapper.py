from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as bs
from utils import beautifyLinkData, beautifyImgdata, summarize


class Scrapper():

    def __init__(self,searchString):
        self.searchString = searchString
        self.url="https://en.wikipedia.org/wiki/"+self.searchString

    def getContent(self):
        uClient = uReq(self.url)
        Page = uClient.read()
        uClient.close()
        html = bs(Page, "html.parser")
        return html

    def getTextdata(self,html):
        info=html.find('div',{'class':"mw-body-content mw-content-ltr"}).find_all('p')
        return summarize(info)

    def getReference(self,html):
        info=html.find('div',{'class':"mw-body-content mw-content-ltr"}).find_all('a',href=True)
        return beautifyLinkData(info,self.searchString)

    def getImages(self,html):
        info=html.find('div',{'class':"mw-body-content mw-content-ltr"}).find_all('img')
        return beautifyImgdata(info)
        
