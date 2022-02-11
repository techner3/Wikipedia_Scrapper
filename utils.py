from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
import base64
import requests
import io
import re
import PIL.Image as Image

def beautifyTextData(info):
    text=''
    for content in info:
        text+=content.text
    text = re.sub(r'\[.*?\]+', '', text)
    text=text.replace('\n', '')
    return text

def summarize(info):
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
    return summary

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
    refList=[]
    for link in info:
        appendLink=beautifyLink(link['href'],searchString)
        refList.append(appendLink)
    return refList

def beautifyImgdata(info):
    imgList=[]
    for imglink in info:
        img=requests.get("https:"+str(imglink['src']),stream = True)
        encodeImg=Imgtobase64(img.content)
        imgList.append(encodeImg)
    return imgList