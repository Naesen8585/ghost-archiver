"""
This will provide the uploading functions to bitchute

general idea: leverage selenium, as bitchute does not have an API, they are probably trying to prevent bot uploads.


"""
import asyncio
import bitchute_client as bc
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
import getpass
import random
import logging
import os
import time
import uuid
from moviepy.editor import *
def login_to_bitchute(email,password):
    url = "https://www.bitchute.com/accounts/login/"
    options = webdriver.ChromeOptions()
    options.add_argument("--incognito")
    options.add_argument("--ignore_certificate_errors")
    #options.add_argument("--headless")
    driver = webdriver.Chrome(chrome_options=options)
    driver.get(url)
    #driver.find_element(By.LINK_TEXT, "Login").click()
    foundelement=False
    while not foundelement:
        #print("Waiting for the login element to fully appear...")
        time.sleep(random.random()+random.randint(2,3))
        foundelement = driver.find_element(By.ID,"id_username")
    #driver.find_element(By.ID, "id_username").click()
    driver.find_element(By.ID, "id_username").send_keys(str(email))
    #driver.find_element(By.ID, "id_password").click()
    driver.find_element(By.ID, "id_password").send_keys(str(password))
    driver.find_element(By.CSS_SELECTOR, ".fa-check:nth-child(1)").click()
    return driver

def generateThumbnail(moviepath):
    clip=VideoFileClip(moviepath)
    imgpath="./"+str(uuid.uuid4())+".png"
    clip.save_frame(imgpath,random.randint(0,int(clip.duration)))
    return imgpath

async def uploadToBitChuteAction(username, password, videopath, thumbnailpath, title, description):
  async with bc.Client() as client:
    await client.login(username, password)
    await client.upload(
        bc.Media.from_file(videopath),
        cover=bc.Media.from_file(thumbnailpath),
        title=title, description=description)

def executeUpload(username,password,videopath,thumbnailpath,title,description):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(uploadToBitChuteAction(username,password,videopath,thumbnailpath,title,description))
    os.remove(thumbnailpath)
    os.remove(videopath)
