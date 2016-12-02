#!/usr/bin/python
# -*- coding: UTF-8 -*-

#
#   This script get the dat from the sgp.aero server and gen the SW JSON file
#
import sys
import json
import urllib2
import datetime
import time
import os
import kpilot
import math
import pycountry
import socket
#-------------------------------------------------------------------------------------------------------------------#
import config

def fixcoding(addr):
        if addr != None:
                addr=addr.replace(u'á', u'a')
                addr=addr.replace(u'à', u'a')
                addr=addr.replace(u'â', u'a')
                addr=addr.replace(u'Á', u'A')
                addr=addr.replace(u'é', u'e')
                addr=addr.replace(u'è', u'e')
                addr=addr.replace(u'ê', u'e')
                addr=addr.replace(u'É', u'E')
                addr=addr.replace(u'í', u'i')
                addr=addr.replace(u'ì', u'i')
                addr=addr.replace(u'î', u'i')
                addr=addr.replace(u'Í', u'I')
                addr=addr.replace(u'ó', u'o')
                addr=addr.replace(u'ò', u'o')
                addr=addr.replace(u'ô', u'o')
                addr=addr.replace(u'Ó', u'O')
                addr=addr.replace(u'Ò', u'O')
                addr=addr.replace(u'ú', u'u')
                addr=addr.replace(u'ù', u'u')
                addr=addr.replace(u'û', u'u')
                addr=addr.replace(u'Ú', u'U')
                addr=addr.replace(u'ü', u'u')
                addr=addr.replace(u'ñ', u'n')
                addr=addr.replace(u'Ñ', u'N')
                addr=addr.replace(u'Ø', u'O')
        return addr

#-------------------------------------------------------------------------------------------------------------------#
#
# arguments:   compid, dayindex, print
#		where compid is the assigned competition ID or 0 for the list of competitions.
#		dayindex is 0 for the first day, 1 second day, etc, ...
#		print is a falg to print the JSON input on pretty print
#

qsgpIDreq=sys.argv[1:]						# first arg is the event ID
dayreq   =sys.argv[2:]						# second arg is the day index within the event
prtreq   =sys.argv[3:]						# print request
 
cucpath="./cuc/"						# directory where to stor the JSON file generated
tp=[]								# turn pint list
tracks=[]							# track list
#

if qsgpIDreq and qsgpIDreq[0] != '0':
	qsgpID   =        sys.argv[1]
	day      =    int(sys.argv[2])
else:
	qsgpID='0'

if prtreq and prtreq[0]=="print":
	prt=True
else:
	prt=False
 
print "Generate .json files V1.0 from  the www.sgp.aero web server"
print "Usage python csgpjson.py COMPID indexday"
hostname=socket.gethostname()
print "DBhost:", config.DBhost, "ServerName:", hostname
start_time = time.time()
local_time = datetime.datetime.now()
j = urllib2.urlopen('http://www.crosscountry.aero/c/sgp/rest/comps/')
j_obj = json.load(j)
if qsgpID == '0':
	#print j_obj
	j=json.dumps(j_obj, indent=4)
	print j
	exit(0)
else:
	for xx in j_obj:
		if xx['id'] == int(qsgpID):
			print "Title:", xx['fullEditionTitle']
	print "CompID:", qsgpID, "Time is now:", local_time     # print the time for information only

fl_date_time = local_time.strftime("%Y%m%d")                    # get the local time
JSONFILE = cucpath + config.Initials + fl_date_time+'.json'            # name of the CUC to be generated
print "JSON generated data file is: ", JSONFILE 		# just a trace
jsonfile = open (JSONFILE, 'w')                                 # open the output file
#
# get the JSON string for the web server
#
j = urllib2.urlopen('http://www.crosscountry.aero/c/sgp/rest/comp/'+str(qsgpID))
j_obj = json.load(j)
if prt:
	#print j_obj
	j=json.dumps(j_obj, indent=4)
	print j
#
# the different pieces of information
#
pilots=j_obj["p"]						# get the pilot information
print "Pilots:", len(pilots)
print "=========="
for id in pilots:
#                        
	pid= 		pilots[id]["i"] 			# get the pilot ID   
	fname= 		pilots[id]["f"]				# first name    
	lname= 		pilots[id]["l"] 			# last name   
	compid= 	pilots[id]["d"]				# competition number    
	country= 	pilots[id]["z"] 			# two letters country code   
	model= 		pilots[id]["s"]				# aircraft model    
	j= 		pilots[id]["j"]    			# ranking list
	rankingid= 	pilots[id]["r"]				# ranking id
	if int(qsgpID) >= 14:
		flarmid= 	pilots[id]["q"]			# flarm id
		registration= 	pilots[id]["w"]			# registration
	else:
		flarmid= 	"FLRDDDDDD"
		registration= 	"EC-XXX"

	rgb=0x111*int(id)                                       # the the RGB color
    	ccc=hex(rgb)                                            # convert it to hex
    	color="#"+ccc[2:]                                       # set the JSON color required
	if hostname == "SWserver":				# deal with the different implementation of pycountry
		ccc = pycountry.countries.get(alpha2=country)	# the the 3 letter country code
    		country=ccc.alpha3				# convert to a 3 letter code
	else:
		ccc = pycountry.countries.get(alpha_2=country)	# the the 3 letter country code
    		country=ccc.alpha_3				# convert to a 3 letter code

	pilotname=fixcoding(fname+" "+lname).encode('utf8')
	print pid, pilotname, compid, country, model, j, rankingid, registration, flarmid    
	# tr={"trackId": config.Initials+fl_date_time+":"+flarmid, "pilotName": pilotname,  "competitionId": compid, "country": country, "aircraft": model, "registration": registration, "3dModel": "ventus2", "ribbonColors":[color], "portraitUrl": "http://rankingdata.fai.org/PilotImages/"+rankingid+".jpg"}
	tr={"trackId": config.Initials+fl_date_time+":"+flarmid, "pilotName": pilotname,  "competitionId": compid, "country": country, "aircraft": model, "registration": registration, "3dModel": "ventus2", "ribbonColors":[color], "portraitUrl": "http://192.168.8.244/pic/"+compid+".jpg"}
	tracks.append(tr)                                       # add it to the tracks

#print tracks
print "Competition"
print "==========="
comp=j_obj["c"]							# get the competition information
comp_firstday		=comp['a']				# first day of the competition
comp_lastday		=comp['b']				# last day of the competition
comp_name		=comp['t']				# event name
comp_shortname		=comp['l']				# event short name
comp_id			=comp['i']
print "Comp ID:", comp_id, "Name:", comp_name, "Short name:", comp_shortname, comp_firstday, comp_lastday
print "Index of Days"
numberofactivedays	=j_obj["j"]
indexofdays		=j_obj["i"]
date			=indexofdays[day]["d"]			# date    
title			=indexofdays[day]["t"] 			# day tittle   
shorttitle		=indexofdays[day]["l"]    		# day short title
starttime		=indexofdays[day]["a"]    		# start time millis from midnite
daytype			=indexofdays[day]["y"]    		# day type: 1, 2, 3 ...
dayid			=indexofdays[day]["i"] 			# day ID 
print date, title, shorttitle, "Start time(millis):", starttime, "Day type:", daytype, "Day ID:", dayid, "Number of active days:", numberofactivedays


d = urllib2.urlopen('http://www.crosscountry.aero/c/sgp/rest/day/'+str(qsgpID)+'/'+str(dayid))
d_obj = json.load(d)
if prt:
	print "____________________________________________________________"
	d=json.dumps(d_obj, indent=4)
	print d
if numberofactivedays == 0:
	print "No active days ..."

print "Day: ", day, "DayID: ", dayid
print "============================="
#print d
comp_day		=d_obj["@type"]
comp_id			=d_obj["e"]				# again the compatition ID
comp_dayid		=d_obj["i"]				# the day ID
comp_date		=d_obj["d"]				# date in milliseconds from the Unix epoch 
comp_daytype		=d_obj["y"]				# day type: 1= valid, 2= practice, 3= canceled, 4= rest, 9= other
comp_daytitle		=d_obj["l"]				# day title
comp_shortdaytitle	=d_obj["t"]				# short day title
comp_starttime		=d_obj["a"]				# start time millis from midnite
comp_startaltitude	=d_obj["h"]				# start altitude
comp_finishaltitude	=d_obj["f"]				# finish altitude
print "Comp day:", comp_day, "Comp ID:", comp_id, "Comp ID DAY:", comp_dayid, "Title:", comp_daytitle, comp_shortdaytitle, "Start time (millis):", comp_starttime, "Start alt.:", comp_startaltitude, "Finish Alt.:", comp_finishaltitude
if "k" in d_obj:
	comp_taskinfo		=d_obj["k"]				# task infor data
else:
	print "No task for that day..."
	exit()
task_type   		=comp_taskinfo["@type"]
task_id  	    	=comp_taskinfo["id"]
task_listid 		=comp_taskinfo["taskListId"]
task_name   		=comp_taskinfo["name"]
task_data   		=comp_taskinfo["data"]

task_at     		=task_data["at"]	
task_wp     		=task_data["g"]	
task_wpla   		=task_data["u"]
task_wptlist		=task_wpla["wptList"]	
print "Task info"
print "========="
print "Tasks type:", task_type, "ID:", task_id, task_listid, "Task Name:", task_name, "Task at:", task_at, task_wptlist,"WP#", len(task_wp)
print "Waypoints of the task"
print "====================="
#
wp=0
while wp < len(task_wp):
		wp_name				=task_wp[wp]["n"]	# waypoint name
		if wp == 0:
			wpinit=wp_name
			type="Start"
		else:
			type="Turnpoint"
		wp_lat				=task_wp[wp]["a"]	# latitude
		wp_lon				=task_wp[wp]["o"]	# longitude
		wp_type				=task_wp[wp]["y"]	# type: line or cylinder
		wp_radius			=task_wp[wp]["r"]	# cylinder radius or line length
		if wp > 0 and  (wp_name == wpinit or wp_type=="line"):
			isbreak=True
			type="Finish"
		if wp_type == "cylinder":
			oz="Cylinder"
		else:
			oz="Line"	
		#wp_id				=task_wp[wp]["id"]	# Wyapoint ID
		print "WP:", wp_name, wp_lat, wp_lon,  wp_type, wp_radius, type, oz
		tpx={"latitude": wp_lat, "longitude": wp_lon, "name": wp_name, "observationZone": oz, "type": type, "radius": wp_radius, "trigger":"Enter"}
        	tp.append(tpx)
		if wp > 0 and  (wp_name == wpinit or wp_type=="line"):
			break
		wp +=1

print "WP:================================>"
# event

print comp_shortname
print comp_name
print comp_date
print comp_starttime/1000
print tp
#event={"name": comp_shortname, "description" : comp_name, "taskType": "SailplaneGrandPrix", "startOpenTs": (comp_date + comp_starttime)/1000, "turnpoints": tp,  "tracks": tracks}
task={ "taskType": "SailplaneGrandPrix", "startOpenTs": comp_date , "turnpoints": tp}
event={"name": comp_shortname, "description" : comp_name, "task" : task , "tracks" : tracks}
j=json.dumps(event, indent=4)
jsonfile.write(j)

#
# close the files and exit
#

jsonfile.close()