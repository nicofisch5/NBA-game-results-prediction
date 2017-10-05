import csv
from init import session
from game import Game
from team import Team
from score import Score
from team_stat import TeamStat


def get_team_ids_by_game_id(game_id):
    team_ids = {}
    rs = session.query(TeamStat).filter_by(game_id=game_id)
    for obj in rs:
        team_ids[obj.ha] = obj.team_id

    return team_ids


def get_wl_ratio_by_team_id(team_id, game_id):
    wl_ratio = {}
    for wl in ['W','L']:
        rs = session.query(TeamStat, Game) \
            .join(Game)\
            .filter(TeamStat.team_id == team_id)\
            .filter(TeamStat.result == wl)\
            .filter(Game.type == 'Season') \
            .filter(Game.id < game_id) \
            .count()

        wl_ratio[wl] = rs

    return wl_ratio


# For each game
# H_won_ratio
# A_Win_ratio
# Div_Conf_Ext
# Result

data = []
index = -1

#rs = session.query(TeamStat).all()
rs = session.query(Game).filter_by(type='Season')

for game in rs:
    index += 1
    data.append(index)
    data[index] = {}
    #print obj.game_id, obj.team_id, obj.ha, obj.result, obj.STLP

    data[index]['dce'] = game.dce
    data[index]['winner'] = game.winner

    # Get team_id of each team
    team_ids = get_team_ids_by_game_id(game.id)

    # Get WL ratio
    hWL = get_wl_ratio_by_team_id(team_ids['H'], game.id)
    aWL = get_wl_ratio_by_team_id(team_ids['A'], game.id)

    data[index]['hWL'] = 0.00
    data[index]['aWL'] = 0.00

    if (hWL['W'] + hWL['L']) > 0:
        data[index]['hWL'] += hWL['W'] / ((1.0 * hWL['W']) + (1.0 * hWL['L']))

    if (aWL['W'] + aWL['L']) > 0:
        data[index]['aWL'] += aWL['W'] / ((1.0 * aWL['W']) + (1.0 * aWL['L']))

    print session.query(Team).get(team_ids['H']).code, data[index]['hWL'], " - ", data[index]['aWL'], session.query(Team).get(team_ids['A']).code

    if index == 200:
        break

#ofile = open('ttest.csv', "wb")
#writer = csv.writer(ofile, delimiter='', quotechar='"', quoting=csv.QUOTE_ALL)

#for row in reader:
#    writer.writerow(row)


#ofile.close()