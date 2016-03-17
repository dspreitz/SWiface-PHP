#!/usr/bin/python
#
# Silent Wings interface --- JSON formaat
#
import json
import time
import sys
import QSGP
import kpilot
import sqlite3
import datetime

cucpath="/var/www/html/cuc/" 
localtime=datetime.datetime.now()
today=localtime.strftime("%y%m%d")
#
#   This script looks into the SWiface database and generates  the fixes to Silent Wing studio
#
arg1=sys.argv[1]
eventid=arg1
id=arg1[0:4]
eventid=arg1[0:12]
dateid=eventid[6:12]

if (today == dateid):
        dbpath='/nfs/OGN/SWdata/';
else:
        dbpath='/nfs/OGN/SWdata/archive/';

if (id == "LIVE"):							# if it a dummy envent LIVE

#	Build the turning points

	tp=[]
	#tp=QSGP.tp

# Build the tracks 
	tracks=[]

#
	conn=sqlite3.connect(dbpath+'SWiface.db')                       # open th DB in read only mode
	cursD=conn.cursor()                                             # cursor for the ogndata table
	cursG=conn.cursor()                                             # cursor for the glider table
	pn=0                                                            # number of pilots found
	cursD.execute('select distinct idflarm from OGNDATA where date = ?', [dateid])           # get all the glifers flying now
	for row in cursD.fetchall():                                    # search all the rows
    		idflarm=row[0]                                          # flarmid is the first field
    		idf=idflarm[3:9]                                        # we skip the first 3 chars
    		cursG.execute("select registration, cn, type from GLIDERS where idglider = ?", [idf])               # search now into the gliding database
    		gli=cursG.fetchone()                                    # get the data from the DB
    		if gli and gli != None:                                 # did we find it ??? Index is unique, only one row
                	regi=gli[0]                                     # get the registration
                	cn=gli[1]                                       # get the competition numbers
                	if cn == "":
                        	cn="XX"                                 # if none ?
       	        	type=gli[2]                                     # get glider type
    		else:
                	regi='NO-NAME'
                	cn='NN'
                	type='NOTYPE'
    		if idflarm in kpilot.kpilot:                            # check if know the pilot because is our database kpilot.py
        		pname=kpilot.kpilot[idflarm]                    # in that case place the name of the pilot
    		else:
        		pname="Pilot NN-"+str(pn)                       # otherwise just say: NoName#
#    		print "D==>: ", idflarm, pname, regi, cn, type
#                                                               write the Pilot detail

    		pn +=1
    
		tr={"trackId": eventid+':'+idflarm, "pilotName": pname,  "competitionId": cn, "country": "ESP", "aircraft": type, "registration": regi, "3dModel": "ventus2", "ribbonColors":["red"]}
		tracks.append(tr)

# event 
	y=int(eventid[4:8])                     # year
        m=int(eventid[8:10])                    # month
        d=int(eventid[10:12])                   # day
        td=datetime.datetime(y,m,d)-datetime.datetime(1970,1,1) # number of second until beginning of the day
        ts=int(td.total_seconds()+9*60*60)      # timestamp 09:00:00 UTC
	event={"name": eventid, "description" : "LIVE Pyrenees",  "eventRevision": 0, "task": { "taskType": "SailplaneGrandPrix", "startOpenTs": ts, "turnpoints" : QSGP.tp },  "tracks": tracks}
	j=json.dumps(event, indent=4)
else:
	datetimes=datetime.datetime.now()
	fname=cucpath+eventid+datetimes.strftime("%Y%m%d")+".json"
	try:
		fd=open(fname, 'r')
		j=fd.read()
		fd.close()
	except:
		j=json.dumps(QSGP.QSGP, indent=4)
		#print "Not found...", fname
print j
