#!/usr/bin/python
#
# configuration for the Silent Wings OGN interface the online part
#

#-------------------------------------
# OGN-Silent Wings interface --- Settings
#-------------------------------------
#
#-------------------------------------
# Setting values from config.ini file
#-------------------------------------
#
import socket
import os
import datetime
from shutil import copyfile
from configparser import ConfigParser
configdir=os.getenv('CONFIGDIR')
if configdir == None:
	configdir='/etc/local/'
configfile=configdir+'SWSconfig.ini'

datafile = open("config.py", "w")
if not os.path.isfile("configtail.txt"):
	print "File Configtail.txt not found, copying configtail.template" 
	copyfile("configtail.template", "configtail.txt")

tailfile = open("configtail.txt", "r")
datafile.write("# SWS configuration file \n")

hostname=socket.gethostname()
datafile.write("# SWS hostname: "+hostname+"\n")
datafile.write("# SWS config file: "+configfile+"\n")
datafile.write("# Config generated: "+datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+" \n")
cfg=ConfigParser()
cfg.read(configfile)

try:
        cucFileLocation = cfg.get('server', 'cucFileLocation').strip("'").strip('"')
except:
        cucFileLocation = "/var/www/html/cuc/"

DBpath                  = cfg.get('server', 'DBpath').strip("'").strip('"')
MySQLtext               = cfg.get('server', 'MySQL').strip("'").strip('"')
DBhost                  = cfg.get('server', 'DBhost').strip("'").strip('"')
DBuser                  = cfg.get('server', 'DBuser').strip("'").strip('"')
DBpasswd                = cfg.get('server', 'DBpasswd').strip("'").strip('"')
try:
	DBuserread      = cfg.get('server', 'DBuserread').strip("'").strip('"')
except:
	DBuserread      = DBuser
try:
	DBpasswdread    = cfg.get('server', 'DBpasswdread').strip("'").strip('"')
except:
	DBpasswdread    = DBpasswd
try:
	SWSserver       = cfg.get('server', 'SWSserver').strip("'").strip('"')
except:
	SWSserver       = 'http://localhost/'
DBname                  = cfg.get('server', 'DBname').strip("'").strip('"')
SQLite3                 = cfg.get('server', 'SQLite3').strip("'").strip('"')
Initials                = cfg.get('server', 'Initials').strip("'").strip('"')

eventname1              = cfg.get('location', 'eventname1').strip("'").strip('"')
eventname2              = cfg.get('location', 'eventname2').strip("'").strip('"')

eventdesc1              = cfg.get('location', 'eventdesc1').strip("'").strip('"')
eventdesc2              = cfg.get('location', 'eventdesc2').strip("'").strip('"')
loclatitude             = cfg.get('location', 'location_latitude').strip("'").strip('"')
loclongitud             = cfg.get('location', 'location_longitud').strip("'").strip('"')
try:
	PicPilots       = cfg.get('location', 'PicPilots').strip("'").strip('"')
except:
	PicPilots	= ' '

datafile.write("cucFileLocation='"+cucFileLocation+"'; \n")
datafile.write("DBpath='"+DBpath+"' \n")
datafile.write("DBhost='"+DBhost+"' \n")
datafile.write("DBname='"+DBname+"' \n")
datafile.write("SQLite3='"+SQLite3+"' \n")
datafile.write("DBuser='"+DBuser+"' \n")
datafile.write("DBpasswd='"+DBpasswd+"' \n")
datafile.write("DBuserread='"+DBuserread+"' \n")
datafile.write("DBpasswdread='"+DBpasswdread+"' \n")
datafile.write("MySQL="+MySQLtext+" \n")
datafile.write("Initials='"+Initials+"' \n")
datafile.write("SWSserver='"+SWSserver+"' \n")
datafile.write("eventname1='"+eventname1+"' \n")
datafile.write("eventname2='"+eventname2+"' \n")
datafile.write("eventdesc1='"+eventdesc1+"' \n")
datafile.write("eventdesc2='"+eventdesc2+"' \n")
datafile.write("loclatitude='"+loclatitude+"' \n")
datafile.write("loclongitud='"+loclongitud+"' \n")
datafile.write("PicPilots='"+PicPilots+"' \n")
# --------------------------------------#
datafile.write(tailfile.read())
datafile.close()
tailfile.close()
