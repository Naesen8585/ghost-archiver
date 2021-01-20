"""
This one will use multiprocessing to handle the uploads from youtube and the ghost archive and dlive simultaneously
"""

import ghost_archiver.tgsArchiver as ta
import getpass
import ghost_archiver.videoFinder as vf
import time
import random
import multiprocessing
DBNAME="./ghost.sqlite"
myuser=input("Enter bitchute username > ")
mypass=getpass.getpass("Enter bitchute password >")

tcrlist=vf.getTCRLinks()
tgslist=vf.getTGSLinks()

tgsprocess=multiprocessing.Process(target=ta.archivetoBitChute,args=(tgslist,myuser,mypass,DBNAME))
tcrprocess=multiprocessing.Process(target=ta.archivetoBitChute,args=(tcrlist,myuser,mypass,DBNAME))

def watcherprocess(myuser,mypass,DBNAME):
    while True:
        dlivelinks=vf.getLinks()
        ta.archivetoBitChute(dlivelinks,myuser,mypass,DBNAME)
        hourstosleep=12
        print("Waiting for "+str(hourstosleep)+" hours...")
        time.sleep(3600*(hourstosleep))

checkerprocess=multiprocessing.Process(target=watcherprocess,args=(myuser,mypass,DBNAME))

tgsprocess.start()
tcrprocess.start()
checkerprocess.start()
