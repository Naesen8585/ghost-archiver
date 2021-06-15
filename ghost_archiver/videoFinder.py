"""
In here we need to get the live links from the DLive "replays" tab. then return them as a list to process later.

"""


from selenium.webdriver.common.by import By
import webdriver_selector
from bs4 import BeautifulSoup
import time
import youtube_dl
import requests

def getTGSLinks(url="https://archive.org/download/theghostshow_202003"):
    page=requests.get(url)
    soup=BeautifulSoup(page.content,'html.parser')
    links=soup.find_all('a')
    linklist=[]
    for link in links:
        if 'href' in link.attrs:
            if not '.ia' in link.attrs['href'] and (
                    '.mp4' in link.attrs['href'] or '.m4v' in link.attrs['href'] or '.mkv' in link.attrs['href']):
                linklist.append("https://archive.org/download/theghostshow_202003/" + link.attrs['href'])
    return linklist

def getLinks(url="https://dlive.tv/ghostpolitics"):

    driver=webdriver_selector(chosendriver="chrome").driver
    driver.get(url)
    time.sleep(5)
    #get the replays link...
    driver.find_element(By.CSS_SELECTOR, ".profile-tab-item:nth-child(3) > .item-label").click()
    html=driver.page_source
    soup=BeautifulSoup(html,'html.parser')
    driver.quit()
    mylinks = soup.find_all('a', attrs={'class': 'd-snap box-block border-radius-5 overflow-hidden'})
    returnlist=[]

    for link in mylinks:
        returnlist.append("https://dlive.tv"+link['href'])
    return returnlist


def getTCRLinks(yt_url="https://www.youtube.com/channel/UClQQG1iLihNl54y1ifRUEYQ/videos"):
    vidlist=[]
    ydl = youtube_dl.YoutubeDL({'outtmpl': '%(id)s%(ext)s', 'quiet': True, 'ignoreerrors': True, })
    vidlist=[]
    with ydl:
        result = ydl.extract_info \
            (yt_url,
             download=False)  # We just want to extract the info
        if 'entries' in result:
            for i, item in enumerate(result['entries']):
                finalurl = result['entries'][i]
                vidlist.append(finalurl['webpage_url'])
        else:
            vidlist.append(result['webpage_url'])


    return vidlist
    #return mylinks
