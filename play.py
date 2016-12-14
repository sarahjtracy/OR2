import nba_py
from nba_py import team
import constants

teamList = team.TeamList().info()
for T in teamList:
  teamId = T['TEAM_ID']
  teamSum = team.TeamSummary(teamId, constants.SEASON).info()
  if (len(teamSum) > 0):
    city = teamSum[0]['TEAM_CITY']
    name = teamSum[0]['TEAM_NAME']
    print str(city), str(name)

