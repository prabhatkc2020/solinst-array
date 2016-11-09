import httplib as http
import urllib
import os
import re
import datetime
import storage.database as lite

def file_list(datadir):
    filelist = []
    for files in os.listdir(datadir):
        matches = re.search("sensordata-[0-9]+\.sqlite", files)
        if (matches):
            filelist.append(files)
            
    return(filelist)

datadir = "data/"

# Determine the name of the current database
today = datetime.datetime.today()
dbdate =  today.strftime('%Y%m%d')
db_filename = "sensordata-" + dbdate + ".sqlite"

# Get list of database files
filelist = file_list(datadir)
for files in filelist:
    sensordb = lite.Database(datadir + files)

    datalist = sensordb.getUnsent()
    if(len(datalist) == 0):
        sensordb.close()
        # Rename file
        if(files != db_filename): 
            newfile = files[:-7] + "_done" + files[-7:]
            os.rename(datadir + files, datadir + newfile)
        continue

    for data in datalist:
        request = {
            'collect_date' : data[0],
            'dht_temp' : data[1],
            'dht_humid' : data[2],
            'soil_temp' : data[3],
            'soil_humid' : data[4],
            'sol_temp' : data[5],
            'sol_depth' : data[6]
        }
    
        conn = http.HTTPConnection("data.sparkfun.com")
        conn.request("GET", "/input/roa2v7VjvaF0gybdZLjp?private_key=jkRvJXpjJRH4eYqlAdPg&" + urllib.urlencode(request))
        r1 = conn.getresponse()
#        print r1.read()
        conn.close()

        if(r1.status != 200):
            continue
        
#        conn.connect()
            
        sensordb.sentData(str(data[0]))
    sensordb.close()



