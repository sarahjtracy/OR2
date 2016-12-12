import constants
import nba_py
from nba_py import team
import player

def getAverage():
  teamList = team.TeamList().info()
  playerList = []
  print(len(teamList))
  for T in teamList:
    abbr = T['ABBREVIATION']
    if (abbr != None): 
      print abbr
      teamId = T['TEAM_ID']
      R = team.TeamCommonRoster(teamId, season=constants.SEASON).roster()
      for P in R:
        playerId = P['PLAYER_ID']
        print playerId
        myPlayer = player.Player(playerId, teamId)
        playerList.append(myPlayer)
  aperTotal = 0
  minutesTotal = 0
  print(len(playerList))
  for P in playerList:
    aper = P.getUPer()
    print P.name, aper
    aperTotal += P.mp * aper
    minutesTotal += P.mp
  return aperTotal/minutesTotal

  return 0
print getAverage()
