"""
In here we need to get the live links from the DLive "replays" tab. then return them as a list to process later.

"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
import chromedriver_binary
from bs4 import BeautifulSoup
import time
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
    options = webdriver.ChromeOptions()
    options.add_argument("--incognito")
    options.add_argument("--ignore_certificate_errors")
    options.add_argument("--headless")
    driver=webdriver.Chrome(chrome_options=options)
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


def getTCRLinks(url="https://www.youtube.com/channel/UClQQG1iLihNl54y1ifRUEYQ/videos"):
    vidlist=[]
    options = webdriver.ChromeOptions()
    options.add_argument("--incognito")
    options.add_argument("--ignore_certificate_errors")
    options.add_argument("--headless")
    driver = webdriver.Chrome(chrome_options=options)
    driver.get(url)
    time.sleep(5)
    #now we have to enumerate all the videos on this playlist...
    for i in range(0,50000,300):
        time.sleep(.01)
        #print(i)
        #time.sleep(5)
        driver.execute_script("window.scrollTo(0,"+str(i)+")")
    html=driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    driver.quit()
    mylinks = soup.find_all('a', attrs={'id': 'video-title'})
    for link in mylinks:
        if "TRUE CAPITALIST RADIO" in str(link.attrs['title']).upper() or "TRUE CONSERVATIVE RADIO" in str(link.attrs['title']).upper():
            vidlist.append("https://www.youtube.com"+str(link.attrs['href']))
    return vidlist
    #return mylinks