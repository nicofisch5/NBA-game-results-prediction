from init import session
from game import Game
from team import Team
from score import Score
from team_stat import TeamStat


rs = session.query(TeamStat).all()

for obj in rs:
    print obj.game_id, obj.team_id, obj.ha, obj.result, obj.STLP