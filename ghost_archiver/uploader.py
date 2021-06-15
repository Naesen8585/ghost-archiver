"""
This will provide the uploading functions to bitchute

general idea: leverage selenium, as bitchute does not have an API, they are probably trying to prevent bot uploads.


"""
import asyncio
import bitchute_client as bc
from selenium.webdriver.common.by import By
import webdriver_selector
import random
import time
import uuid
from moviepy.editor import *
import os

def login_to_bitchute(email,password):
    url = "https://www.bitchute.com/accounts/login/"

    driver = webdriver_selector.selector(chosendriver="chrome").driver
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
        while True:
            try:
                await client.login(username, password)
                await client.upload(
                    bc.Media.from_file(videopath),
                    cover=bc.Media.from_file(thumbnailpath),
                    title=title, description=description)
                break
            except asyncio.TimeoutError:
                print("Timeout error...trying again")
                time.sleep(5)

def executeUpload(username,password,videopath,thumbnailpath,title,description):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(uploadToBitChuteAction(username,password,videopath,thumbnailpath,title,description))
    os.remove(thumbnailpath)
    os.remove(videopath)
