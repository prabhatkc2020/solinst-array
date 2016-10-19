# Class to manage database storage

import sqlite3 as lite
# import datetime
# import sys
import os


class Database:
    def __init__(self, dbfile):
        self.dbfile = dbfile

        self.connect()

    def connect(self):
        # TODO: Add some error detection
        fileInit = True
        if (os.path.exists(self.dbfile)):
            fileInit = False

        self.con = lite.connect(self.dbfile)

        if(fileInit):
            self.initTable()

    def addLine(self, data):
        # sanity check on the data
        if(len(data) != 5):
            return -1

        query="INSERT INTO sensor_data(sensor_serial, sensor_db, sensor_gl, sensor_humid, sensor_wind) VALUES(?, ?, ?, ?, ?)"
        cur = self.con.cursor()

        try:
            cur.execute(query, (data[0], data[1], data[2], data[3], data[4]))
            self.con.commit()
        except lite.Error, e:
            if self.con:
                self.con.rollback()
            print "Error %s:" % e.args[0]
            return(-1)

        return(0)

    def getUnsent(self):
        query = "SELECT * FROM sensor_data WHERE transmit='FALSE'"
        cur = self.con.cursor()

        try:
            cur.execute(query)
            self.con.commit()
        except lite.Error, e:
            if self.con:
                self.con.rollback()
            print "Error %s:" % e.args[0]
            return(-1)
        
        rows = cur.fetchall()
        return(rows)
    
    def sentData(self, serial, raw_date):
        collect_date = raw_date.strftime("%Y-%m-%d %H:%M:%S")
        query = "UPDATE sensor_data SET transmit='TRUE' WHERE collect_date=? AND sensor_serial=?"
        cur = self.con.cursor() 

        try:
            cur.execute(query, (collect_date, serial))
            self.con.commit()
        except lite.Error, e:
            if self.con:
                self.con.rollback()
            print "Error %s:" % e.args[0]
            return(-1)

        return(0)
        
    def initTable(self):
        query = 'DROP TABLE IF EXISTS sensor_data; CREATE TABLE sensor_data ("collect_date" DATETIME PRIMARY KEY  NOT NULL  DEFAULT (CURRENT_TIMESTAMP) ,"sensor_serial" VARCHAR(16) NOT NULL ,"sensor_db" REAL NOT NULL ,"sensor_gl" REAL NOT NULL ,"sensor_humid" REAL NOT NULL ,"sensor_wind" REAL NOT NULL , "transmit" BOOL NOT NULL  DEFAULT FALSE)'
        cur = self.con.cursor()  

        try:
            cur.executescript(query)                
            self.con.commit()
        except lite.Error, e:
            if self.con:
                self.con.rollback()
        
            print "Error %s:" % e.args[0]
            return(-1)
        
        return(0)

    def close(self):
        self.con.close()