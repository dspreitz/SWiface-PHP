# SWS configuration file 
# SWS hostname: SWserver
# Config generated: 2016-11-23 12:00:21 
DBpath='/nfs/OGN/SWdata/' 
DBhost='casadonfs' 
DBuser='ogn' 
DBname='SWIFACE' 
DBpasswd='ogn' 
MySQL=True 
# --------------------------------------#

# default event if no JSON file found  

tp1={"latitude": 42.3868, "longitude": 1.8683, "name": "LECD", "observationZone": "Line", "type": "Start", "radius": 1000, "trigger":"Enter"}
tp2={"latitude": 42.5675, "longitude": -0.72566, "name": "LECI", "observationZone": "Cylinder", "type": "Turnpoint", "radius": 500, "trigger":"Enter"}
tp3={"latitude": 42.3868, "longitude": 1.8683, "name": "LECD", "observationZone": "Line", "type": "Finish", "radius": 1000, "trigger":"Enter"}
tr1={"trackId": "FLRDDE421", "pilotName": "Juanma Garete ", "competitionId": "T1", "country": "ES", "aircraft": "Duo Discus", "registration": "EC-JAA", "3dModel": "ventus2", "ribbonColors":["green"]}
tr2={"trackId": "FLRDDE1FC", "pilotName": "Sergi Pujol", "competitionId": "SP", "country": "FR", "aircraft": "Duo Discus", "registration": "D-1234", "3dModel": "ventus2", "ribbonColors":["blue"]}
tr3={"trackId": "FLRDDDB8B", "pilotName": "Luis Ferreira", "competitionId": "AA", "country": "ES", "aircraft": "Duo Discus", "registration": "EC-JAA", "3dModel": "ventus2", "ribbonColors":["green"]}
tr4={"trackId": "FLRDDBC42", "pilotName": "Santa Cilia ", "competitionId": "T1", "country": "ES", "aircraft": "Duo Discus", "registration": "EC-JAA", "3dModel": "ventus2", "ribbonColors":["green"]}
tr5={"trackId": "FLRDDC1AC", "pilotName": "Angel Casado", "competitionId": "K5", "country": "ES", "aircraft": "Janus CE", "registration": "D-2520", "3dModel": "ventus2", "ribbonColors":["red"]}
QSGP={"name": "QSGP La Cerdanya", "description": "Day 1", "taskType": "SailplaneGrandPrix", "startOpenTs": 0, "turnpoints": [tp1, tp2, tp3], "tracks": [tr1, tr2, tr3, tr4, tr5]}

tp = [
        {
            "name": "Cerdanya",
            "trigger": "Enter",
            "longitude": 1.863883278972198,
            "observationZone": "Line",
            "radius": 3000,
            "latitude": 42.3875017060334,
            "type": "Start"
        },
        {
            "name": "E05/Santa Cilia",
            "trigger": "Enter",
            "longitude": -0.7433333293538958,
            "observationZone": "Cylinder",
            "radius": 3000,
            "latitude": 42.569717492711,
            "type": "Turnpoint"
        },
        {
            "name": "E18/Benabarre",
            "trigger": "Enter",
            "longitude": 0.4827833303850359,
            "observationZone": "Cylinder",
            "radius": 3000,
            "latitude": 42.022216359031944,
            "type": "Turnpoint"
        },
        {
            "name": "Cerdanya",
            "trigger": "Enter",
            "longitude": 1.8638888285008988,
            "observationZone": "Cylinder",
            "radius": 3000,
            "latitude": 42.3875017060334,
            "type": "Finish"
        },
    ]


