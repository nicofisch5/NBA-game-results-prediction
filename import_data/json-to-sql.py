import os
import json
import mysql.connector 
from constants import STATS


def load_json(filename):
    if filename.endswith(".json"):
        return json.loads(open(filename).read())
    return -1


def get_team_id_by_name(teamName):
    cursor.execute("SELECT id FROM team WHERE name='" + teamName + "';")
    return cursor.fetchone()


def get_dce_by_teams_names(home_team_name, away_team_name):
    cursor.execute("SELECT division,conference FROM team WHERE name='" + home_team_name + "';")
    home_team_d_c = cursor.fetchone()

    cursor.execute("SELECT division,conference FROM team WHERE name='" + away_team_name + "';")
    away_team_d_c = cursor.fetchone()

    dce = 'E'
    if home_team_d_c[0] == away_team_d_c[0]:
        dce = 'D'
    elif home_team_d_c[1] == away_team_d_c[1]:
        dce = 'C'

    return dce


season = "2010-2011"
directory = "/var/www/basketball_reference/matches/united_states/nba/" + season

gameNode = ["code","season","date","time","type"]
haNode = {
    "home": 'H',
    "away": 'A',
}

conn = mysql.connector.connect(host="localhost",user="root",password="xy46oi03", database="NBA-games")
cursor = conn.cursor()

fileList = sorted(os.listdir(directory))

for filename in fileList:
    jsonData = load_json(directory + '/' + filename)
    if jsonData != -1:
        sqlQueryColumns = "INSERT INTO game("
        sqlQueryValues = " VALUES("

        # Game winner
        hPTS = jsonData["home"]["totals"]["PTS"]
        aPTS = jsonData["away"]["totals"]["PTS"]
        winner = 'H'
        if aPTS > hPTS:
            winner = 'A'

        # Game DCE
        dce = get_dce_by_teams_names(
            jsonData["home"]["name"],
            jsonData["away"]["name"]
        )

        for node in gameNode:
            sqlQueryColumns += node + ","
            sqlQueryValues += "'" + jsonData[node] + "',"

        sqlQueryColumns += "dce,winner)"
        sqlQueryValues += "'" + dce + "','" + winner + "');"

        cursor.execute(sqlQueryColumns + sqlQueryValues)

        gameId = cursor.lastrowid

        # Stat ans score
        for node in haNode:
            teamId = get_team_id_by_name(jsonData[node]["name"])

            # Game result
            result = 'W'
            if (node == 'away' and aPTS < hPTS) or (node == 'home' and hPTS < aPTS):
                result = 'L'

            # Stat
            sqlQueryColumns = "INSERT INTO stat(game_id,ha,team_id,result,"
            sqlQueryValues = " VALUES(" + str(gameId) + ",'" + haNode[node] + "'," + str(teamId[0]) + ",'" + result + "',"

            for subNode in jsonData[node]["totals"]:
                sqlQueryColumns += "`" + STATS[subNode] + "`,"
                sqlQueryValues += "'" + str(jsonData[node]["totals"][subNode]) + "',"

            sqlQueryColumns = sqlQueryColumns[:-1] + ")"
            sqlQueryValues = sqlQueryValues[:-1] + ");"

            cursor.execute(sqlQueryColumns + sqlQueryValues)

            # Score
            for subNode in jsonData[node]["scores"]:
                sqlQueryColumns = "INSERT INTO score(game_id,period,ha,score)"
                sqlQueryValues = " VALUES(" + str(gameId) + ",'" + str(subNode) + "','" + haNode[node] + "'," + jsonData[node]["scores"][subNode] + ");"

                cursor.execute(sqlQueryColumns + sqlQueryValues)

        conn.commit()

        continue
    else:
        continue

cursor.close()
conn.close()
