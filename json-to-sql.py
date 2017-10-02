import os
import json

def loadJSON(filename):
    if filename.endswith(".json"):
        return json.loads(open(filename).read())
    return -1

directory = '/var/www/basketball_reference/matches/united_states/nba/2010-2011'

for filename in os.listdir(directory):
    jsonData = loadJSON(directory + '/' + filename)
    if jsonData != -1:
        print jsonData
        break;
        continue
    else:
        continue

