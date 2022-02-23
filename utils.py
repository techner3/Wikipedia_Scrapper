from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
import base64
import requests
import re
import pandas as pd
from logger import getLog

logger=getLog('Utils.py')

def beautifyTextData(info):

    try:
        text=''
        for content in info:
            text+=content.text
        text = re.sub(r'\[.*?\]+', '', text)
        text=text.replace('\n', '')
        logger.info('Text data beautified')
        return text
    except Exception as e:
        logger.exception(f"Failed to beautify Text data: \n{e}")

def summarize(info):
    
    try:
        text=beautifyTextData(info)
        stopWords = set(stopwords.words("english"))
        words = word_tokenize(text)
        freqTable = dict()

        for word in words:
            word = word.lower()
            if word in stopWords:
                continue
            if word in freqTable:
                freqTable[word] += 1
            else:
                freqTable[word] = 1

        sentences = sent_tokenize(text)
        sentenceValue = dict()

        for sentence in sentences:
            for word, freq in freqTable.items():
                if word in sentence.lower():
                    if sentence in sentenceValue:
                        sentenceValue[sentence] += freq
                    else:
                        sentenceValue[sentence] = freq
        sumValues = 0

        for sentence in sentenceValue:
            sumValues += sentenceValue[sentence]
        average = int(sumValues / len(sentenceValue))
        summary = ''

        for sentence in sentences:
            if (sentence in sentenceValue) and (sentenceValue[sentence] > (1.2 * average)):
                summary += " " + sentence
        logger.info("Text data summarized")
        return summary
    except Exception as e:
        logger.exception("Failed to summarize text data : \n{e}")

def Imgtobase64(img):

    encodedImg=base64.b64encode(img)
    return encodedImg

def beautifyLink(textLink,searchString):

    if "http" not in textLink:
            if "#" in textLink:
                appendLink="https://en.wikipedia.org/"+searchString+"/"+str(textLink)
            elif "wiki" in textLink:
                appendLink="https://en.wikipedia.org/"+str(textLink)
            else:
                appendLink="https://"+str(textLink)
    else:
        appendLink=textLink
    return appendLink
        
def beautifyLinkData(info,searchString):
    
    try:
        refList=[]
        for link in info:
            appendLink=beautifyLink(link['href'],searchString)
            refList.append(appendLink)
        logger.info("Link data beautified")
        return refList
    except Exception as e:
        logger.exception(f"Failed to beautify link data: \n{e}")

def beautifyImgdata(info):
    
    try:
        imgList=[]
        for imglink in info:
            img=requests.get("https:"+str(imglink['src']),stream = True)
            encodeImg=Imgtobase64(img.content)
            imgList.append(encodeImg)
        logger.info("Image data beautfied")
        return imgList
    except Exception as e:
        logger.exception(f"Failed to beautify image data: \n{e}")

def Dict_DF(data):

    return pd.DataFrame(data)