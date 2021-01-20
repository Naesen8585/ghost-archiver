import ghost_archiver.tgsArchiver as ta
import getpass
import ghost_archiver.videoFinder as vf
DBNAME="./ghost.sqlite"

class tcr_archive:
    def __init__(self,bitchuteuser=None,bitchutepass=None,DBNAME=DBNAME):
        if bitchuteuser is None:
            self.bitchuteuser = input("Enter bitchute username > ")
        if bitchutepass is None:
            self.bitchutepass = getpass.getpass("Enter bitchute password >")
        self.tcrlist = vf.getTCRLinks()
        ta.archivetoBitChute(self.tcrlist,self.bitchuteuser,self.bitchutepass,DBNAME)

class tgs_archive:
    def __init__(self,bitchuteuser=None,bitchutepass=None,DBNAME=DBNAME):
        if bitchuteuser is None:
            self.bitchuteuser = input("Enter bitchute username > ")
        if bitchutepass is None:
            self.bitchutepass = getpass.getpass("Enter bitchute password >")
        self.tgslist = vf.getTGSLinks()
        ta.archivetoBitChute(self.tgslist,self.bitchuteuser,self.bitchutepass,DBNAME)

class dlive_archive:
    def __init__(self,bitchuteuser=None,bitchutepass=None,DBNAME=DBNAME):
        if bitchuteuser is None:
            self.bitchuteuser = input("Enter bitchute username > ")
        if bitchutepass is None:
            self.bitchutepass = getpass.getpass("Enter bitchute password >")
        self.dlivelinks = vf.getLinks()
        ta.archivetoBitChute(self.dlivelinks, self.bitchuteuser, self.bitchutepass, DBNAME)