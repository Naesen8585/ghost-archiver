"""
This will focus on transferring all of the existing TGS shows from the archive to bitchute


"""

import requests
from bs4 import BeautifulSoup
from vidDownloader import *
from dbmanager import *
import hashlib
import glob
import uploader
import getpass
import os
#DBNAME="./tgsdb.sqlite"

def archivetoBitChute(urlList,myuser,mypass,DBNAME):
    #tableGenerator(DBNAME)
    #urlList = vidlistmaker
    for url in urlList:
        viddata = downloader(url)
        filestring = viddata.hookdata['filename'].split('.')[0]
        finalfilename = None
        for file in glob.glob("./" + filestring + "*"):
            finalfilename = file
        hash = hashlib.md5(open(finalfilename, 'rb').read()).hexdigest()
        if not geturlvalue(DBNAME, hash) >= 1:
            thumbnailpath = uploader.generateThumbnail(finalfilename)
            vidname = filestring.replace("_", " ")
            uploader.executeUpload(myuser, mypass, finalfilename, thumbnailpath, vidname, vidname)
            updatedb(DBNAME, hash)
        else:
            os.remove(finalfilename)
