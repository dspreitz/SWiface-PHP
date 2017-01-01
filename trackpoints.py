#!/usr/bin/python
#
# Silent Wings interface --- JSON formaat
#
 
import json
import sqlite3
import MySQLdb 
import datetime
import time
import sys
import os
import config


#
#   This script looks into the SWiface database and generates  the fixes to Silent Wing studio
#

id=sys.argv[1]
trackid=id[id.find(':')+1:]
eventid=id[0:12]
since  =sys.argv[2]
live=True
DBname=config.DBname

localtime=datetime.datetime.now()
today=localtime.strftime("%y%m%d")
date="0"
time="0"
if (since == "0"):
	date=eventid[6:12]
	
else:
	datetimes=datetime.datetime.utcfromtimestamp(int(since))	# time converted from UNIX timestamp
	date =     datetimes.strftime("%y%m%d")				# date converted
	time =     datetimes.strftime("%H%M%S")				# time converted
	datetimet=datetime.datetime.utcnow() - datetime.timedelta(0,15) # UTC time minos 15 seconds for buffering 
	timet =    datetimet.strftime("%H%M%S")				# UTC now minos 15 seconds


if (today != date):						# it is today
	dbpath=config.DBpath+'/archive/';			# no user archive folder
	live=False						# mark as NOT live
	DBname='SWARCHIVE'
else:
	dbpath=config.DBpath

#print trackid,":", eventid,":", since,":", date,":", time

if (config.MySQL):
	conn=MySQLdb.connect(host=config.DBhost, user=config.DBuser, passwd=config.DBpasswd, db=DBname)     # connect with the database
else:

	filename=dbpath+'SWiface.db'		                # open th DB in read only mode
	fd = os.open(filename, os.O_RDONLY)
	conn = sqlite3.connect('/dev/fd/%d' % fd)

cursD=conn.cursor()                                             # cursor for the ogndata table
if (since == "0"):						# if no timme since showw all
	cursD.execute("select date, time, longitude, latitude, altitude  from OGNDATA where idflarm = '%s' and date = '%s' ;" % (trackid,date))   # get all the positions now
else:
	cursD.execute("select date, time, longitude, latitude, altitude  from OGNDATA where idflarm = '%s' and date = '%s' and time > '%s' and time <= '%s'  order by time" %  (trackid, date, time, timet))           

tn=0
#tracks=[{"t":0, "n":0, "e":0, "a":0}]
tracks=[]

for row in cursD.fetchall(): 
	date=row[0]
	y=int(date[0:2])+2000
	M=int(date[2:4])
	d=int(date[4:6])
	time=row[1]
	h=int(time[0:2])
	m=int(time[2:4])
	s=int(time[4:6])
	dt=datetime.datetime(y,M,d,h,m,s)
	ts=(dt - datetime.datetime(1970, 1, 1)).total_seconds()
	long=row[2]
	lati=row[3]
	alti=row[4]
	#print "T==>", tn, date, time, trackid, lati, long, alti, dt, ts
	tracks.append({"t": int(ts), "e":long, "n":lati, "a":alti})
	tn +=1

tp={"trackId": id, "live": live, "track": tracks}
j=json.dumps(tp, indent=4)
print j
conn.close()
if ( not config.MySQL):
	os.close(fd)
