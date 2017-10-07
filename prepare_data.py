import csv
from datetime import datetime, timedelta
from init import session
from game import Game
from team import Team
from score import Score
from team_stat import TeamStat
from sqlalchemy.sql import func, desc


def get_team_ids_by_game_id(game_id):
    team_ids = {}
    rs = session.query(TeamStat).filter_by(game_id=game_id)
    for obj in rs:
        team_ids[obj.ha] = obj.team_id

    return team_ids


def get_last_game_ids_by_team_id(team_id, game_id, nb_of_games=82):
    rs_game_ids = session.query(Game.id) \
        .join(TeamStat) \
        .filter(TeamStat.team_id == team_id) \
        .filter(Game.type == 'Season') \
        .filter(Game.id < game_id) \
        .order_by(desc(Game.date)) \
        .limit(nb_of_games) \
        .all()

    game_ids = []
    for game_id in rs_game_ids:
        game_ids.append(str(game_id[0]))

    return game_ids


def get_wl_ratio_by_team_id(team_id, game_id, nb_of_games=82):
    result = {'W': 0, 'L': 0}

    game_ids = get_last_game_ids_by_team_id(team_id, game_id, nb_of_games)
    if not game_ids:
        return result

    rs = session.query(TeamStat.result, func.count(Game.id))\
        .join(Game)\
        .filter(TeamStat.team_id == team_id) \
        .filter(Game.type == 'Season') \
        .filter(Game.id.in_(game_ids)) \
        .group_by(TeamStat.result) \
        .all()

    for row in rs:
        result[row[0]] = row[1]

    return result


def get_eFGP_by_team_id(team_id, game_id, nb_of_games=82):
    game_ids = get_last_game_ids_by_team_id(team_id, game_id, nb_of_games)
    if not game_ids:
        game_ids = [0]

    rs = session.query(
            func.sum(TeamStat.FG).label("FG"),
            func.sum(TeamStat.b3P).label("b3P"),
            func.sum(TeamStat.FGA).label("FGA"),
        ) \
        .join(Game)\
        .filter(TeamStat.team_id == team_id) \
        .filter(Game.type == 'Season') \
        .filter(Game.id.in_(game_ids)) \
        .one()

    return rs


def get_nb_of_games_by_team_id(team_id, game_id, nb_of_days):
    # Dates
    game = session.query(Game).get(game_id)
    to_date = game.date
    from_date = game.date - timedelta(days=nb_of_days)

    rs = session.query(Game, TeamStat) \
        .join(TeamStat) \
        .filter(TeamStat.team_id == team_id) \
        .filter(Game.type == 'Season') \
        .filter(Game.date >= from_date) \
        .filter(Game.date < to_date) \
       .count()

    return rs



data = []
index = -1

#rs = session.query(TeamStat).all()
rs = session.query(Game).filter_by(type='Season')

for game in rs:
    index += 1
    data.append(index)
    data[index] = []
    #print obj.game_id, obj.team_id, obj.ha, obj.result, obj.STLP

    data[index].append(game.dce)

    # Get team_id of each team
    team_ids = get_team_ids_by_game_id(game.id)

    # Get WL ratio
    hWL = get_wl_ratio_by_team_id(team_ids['H'], game.id, 8)
    aWL = get_wl_ratio_by_team_id(team_ids['A'], game.id, 8)

    hWL_ratio = 0.00
    aWL_ratio = 0.00

    if (hWL['W'] + hWL['L']) > 0:
        hWL_ratio += hWL['W'] / ((1.0 * hWL['W']) + (1.0 * hWL['L']))

    if (aWL['W'] + aWL['L']) > 0:
        aWL_ratio += aWL['W'] / ((1.0 * aWL['W']) + (1.0 * aWL['L']))

    data[index].append(round(hWL_ratio, 2))
    data[index].append(round(aWL_ratio, 2))
    data[index].append(round(hWL_ratio - aWL_ratio, 2))

    # eFG% = (FG + (0.5 x b3P)) / FGA
    h_eFGP = get_eFGP_by_team_id(team_ids['H'], game.id, 8)
    if h_eFGP[0] is not None:
        h_eFGP = round((float(h_eFGP[0]) + (0.5 * float(h_eFGP[1]))) / float(h_eFGP[2]), 3)
    else:
        h_eFGP = -1

    a_eFGP = get_eFGP_by_team_id(team_ids['A'], game.id, 8)
    if a_eFGP[0] is not None:
        a_eFGP = round((float(a_eFGP[0]) + (0.5 * float(a_eFGP[1]))) / float(a_eFGP[2]), 3)
    else:
        a_eFGP = -1

    # Team's names
    #data[index].append(session.query(Team).get(team_ids['H']).code)
    #data[index].append(session.query(Team).get(team_ids['A']).code)

    # eFGP
    data[index].append(h_eFGP)
    data[index].append(a_eFGP)
    data[index].append(round(h_eFGP - a_eFGP, 3))

    # Tiredness
    data[index].append(
        get_nb_of_games_by_team_id(team_ids['H'], game.id, 4)
        - get_nb_of_games_by_team_id(team_ids['A'], game.id, 4)
    )

    # Result
    data[index].append(game.winner)

#    if index == 100:
#        break

#for row in data:
#    print row


ofile = open('NBA-games-winRatio8_eFGP8_tirednessDiff4.arff', "a")
writer = csv.writer(ofile, delimiter=',')

for row in data:
    writer.writerow(row)

ofile.close()