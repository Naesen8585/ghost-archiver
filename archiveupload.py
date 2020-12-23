"""
This one will use multiprocessing to handle the uploads from youtube and the ghost archive and dlive simultaneously
"""

import tgsArchiver
import getpass
import videoFinder
import time
import random
import multiprocessing
DBNAME="./ghost.sqlite"
myuser=input("Enter bitchute username > ")
mypass=getpass.getpass("Enter bitchute password >")

tcrlist=videoFinder.getTCRLinks()
tgslist=videoFinder.getTGSLinks()

tgsthread=multiprocessing.Process(target=tgsArchiver.archivetoBitChute,args=(tgslist,myuser,mypass,DBNAME))
tcrthread=multiprocessing.Process(target=tgsArchiver.archivetoBitChute,args=(tcrlist,myuser,mypass,DBNAME))

def watcherthread(myuser,mypass,DBNAME):
    while True:
        dlivelinks=videoFinder.getLinks()
        tgsArchiver.archivetoBitChute(dlivelinks,myuser,mypass,DBNAME)
        hourstosleep=random.randint(6,24)
        print("Waiting for "+str(hourstosleep)+" hours...")
        time.sleep(3600*(random.randint(6,24)))

checkerthread=multiprocessing.Process(target=watcherthread,args=(myuser,mypass,DBNAME))

tgsthread.start()
tcrthread.start()
checkerthread.start()
