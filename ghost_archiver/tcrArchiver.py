"""

This will focus on putting True Capitalist Radio up on Bitchute, transferred from Youtube.

"""

import ghost_archiver.uploader as uploader
import ghost_archiver.videoFinder as videoFinder
from ghost_archiver.vidDownloader import *
from ghost_archiver.dbmanager import *
import hashlib
import glob
import getpass

DBNAME="./tcrdb.sqlite"
tableGenerator(DBNAME)

myuser=input("Please enter user for bitchute >")
mypass=getpass.getpass("Please enter pass for bitchute >")

urlList=videoFinder.getTCRLinks()
for url in urlList:
    viddata=downloader(url)
    filestring=viddata.hookdata['filename'].split('.')[0]
    finalfilename=None
    for file in glob.glob("./"+filestring+"*"):
        finalfilename=file
    hash=hashlib.md5(open(finalfilename,'rb').read()).hexdigest()
    if not geturlvalue(DBNAME,hash) >= 1:
        thumbnailpath=uploader.generateThumbnail(finalfilename)
        vidname=filestring.replace("_"," ")
        uploader.executeUpload(myuser,mypass,finalfilename,thumbnailpath,vidname,vidname)
        updatedb(DBNAME,hash)




