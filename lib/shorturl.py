# -*- coding: utf-8 -*-

import hashlib
import string
import config
import psycopg2 as pg

class shortURL:
    conn = None
    def __init__(self):
        pass

    def addRouteToDatabase(self,lonMap,latMap,zoom,lonStart,latStart,lonDest,latDest,addressStart,addressDest):
        c = config.Config()
        try:
            tmp = ("dbname=%s user=%s password=%s host=%s") % ( c.dbname, c.dbuser, c.dbpassword, c.host )
            self.conn = pg.connect( tmp );
        except:
            print "I am unable to connect to the database"
        h = hashlib.md5()
        h.update(addressStart.encode("utf-8"))
        h.update(addressDest.encode("utf-8"))
        h.update(str(lonStart))
        h.update(str(latStart))
        h.update(str(lonDest))
        h.update(str(latDest))
        h.update(str(lonMap))
        h.update(str(latMap))
        h.update(str(zoom))
        cur = self.conn.cursor()
        query = "INSERT INTO " + c.tableURL + "(\"id\", \"zoom\", \"lonMap\", \"latMap\", \"lonStart\", \"latStart\", \"lonDest\", \"latDest\", \"addressStart\", \"addressDest\") VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
	try:        
	    cur.execute( query , [ h.hexdigest()[0:16], zoom, lonMap, latMap, lonStart, latStart, lonDest, latDest, addressStart, addressDest ] )
	except Exception as ex:
            print "I am unable to insert data into the database"
            print ex
        self.conn.commit()
        self.conn.close()
        return h.hexdigest()[0:16]

    def hashExists(self,value):
	res = False        
	c = config.Config()
        try:
            tmp = ("dbname=%s user=%s password=%s host=%s") % ( c.dbname, c.dbuser, c.dbpassword, c.host )
            self.conn = pg.connect( tmp );
        except:
            print "I am unable to connect to the database"
        cur = self.conn.cursor()
        query = ("SELECT COUNT(*) as nb FROM %s WHERE id='%s'") % ( c.tableURL, value) 
	try:        
	    cur.execute( query )
	except Exception as ex:
            print "I am unable to verify if hash exists in the database"
            print ex
        if( int(cur.fetchone()[0]) == 0 ):
            res = False
        else:
            res = True
        self.conn.close()
        return res

    def getDataFromHash(self,value):
        if( not self.hashExists(value) ):
            return []
        else:
            c = config.Config()
            try:
                tmp = ("dbname=%s user=%s password=%s host=%s") % ( c.dbname, c.dbuser, c.dbpassword, c.host )
                self.conn = pg.connect( tmp );
            except:
                print "I am unable to connect to the database"
            cur = self.conn.cursor()
            query = ("SELECT * FROM %s WHERE id='%s'") % ( c.tableURL, value) 
	    try:        
	        cur.execute( query )
	    except Exception as ex:
                print "I am unable to read data from the database"
                print ex
            tmp = cur.fetchone()
            self.conn.close()
            return tmp

