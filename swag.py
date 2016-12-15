import requests
import json


playerId = 2544
HUSTLE_URL = 'http://stats.nba.com/stats/leaguehustlestatsplayer?PlayerID=2544&LastNGames=0&LeagueID=00&Month=0&OpponentTeamID=0&PORound=0&PaceAdjust=N&PerMode=PerGame&Period=0&PlusMinus=N&Rank=N&Season=2016-17&SeasonType=Regular+Season&Weight=' 
r = requests.get(HUSTLE_URL)
d = json.loads(r.content)['resultSets'][0]['rowSet']
hs = filter(lambda x: x[0] == playerId, d)[0]
print hs
