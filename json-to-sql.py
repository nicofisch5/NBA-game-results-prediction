import os
import json
import mysql.connector 
from constants import STATS


def loadJSON(filename):
    if filename.endswith(".json"):
        return json.loads(open(filename).read())
    return -1

season = "2010-2011"
directory = "/var/www/basketball_reference/matches/united_states/nba/" + season

gameNode = ["code","season","date","time","type"]
haNode = ["home","away"]
statNode

conn = mysql.connector.connect(host="localhost",user="root",password="xy46oi03", database="NBA-games")
cursor = conn.cursor()

for filename in os.listdir(directory):
    jsonData = loadJSON(directory + '/' + filename)
    if jsonData != -1:
        sqlQueryColumns = "INSERT INTO game("
        sqlQueryValues = " VALUES("

        for node in gameNode:
            sqlQueryColumns += node + ","
            sqlQueryValues += "'" + jsonData[node] + "',"

        sqlQueryColumns = sqlQueryColumns[:-1] + ")"
        sqlQueryValues = sqlQueryValues[:-1] + ");"

        #print sqlQueryColumns + sqlQueryValues
        cursor.execute(sqlQueryColumns + sqlQueryValues)

        gameId = conn.insert_id()

        

        conn.commit()

        continue
    else:
        continue

cursor.close()
conn.close()