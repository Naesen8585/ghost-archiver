'''
This will handle the database ops for the archiver
'''

import sqlitedict
import sys
sys.setrecursionlimit(1500)

def tableGenerator(dbname):

    try:
        database_dict = sqlitedict.SqliteDict(dbname,autocommit=True,tablename='UPLOADS')
        #we're going to handle this using a md5 : useage dictionary
        database_dict['MD5']='UPLOADED'
        print("table Created!")
        updatesuccess=True
    except Exception as e:
        print(e)



def updatedb(dbname,url):
    try:
        database_dict = sqlitedict.SqliteDict(dbname, autocommit=True, tablename='UPLOADS')
        if url in database_dict.keys():
            tempvalue=database_dict.get(url)
            tempvalue=1
            database_dict[url]=tempvalue
        else:
            database_dict[url]=0
            updatedb(dbname,url)
    except:
        print("could not update db")


def geturlvalue(dbname,url):
    try:
        database_dict = sqlitedict.SqliteDict(dbname, autocommit=True, tablename='UPLOADS')
        if url in database_dict.keys():
            tempvalue=database_dict.get(url)
            return tempvalue
        else:
            return -1
    except:
        return -1
        print("could not check db")