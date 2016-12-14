import constants
import nba_py
from nba_py import team
import player
import team
import league

def getAverage():
  pulledTeamList = nba_py.team.TeamList().info()
  playerList = []
  teamList = []
  #print(len(teamList))

  # INITIALIZE TEAMS AND ROSTERS
  for T in pulledTeamList:
    abbr = T['ABBREVIATION']
    if (abbr != None): 
      #print abbr
      teamId = T['TEAM_ID']
      R = nba_py.team.TeamCommonRoster(teamId, season=constants.SEASON).roster()
      teamPlayers = [] 
      for P in R:
        playerId = P['PLAYER_ID']
        myPlayer = player.Player(playerId, teamId)
        teamPlayers.append(myPlayer)
        playerList.append(myPlayer)
      myTeam = team.Team(teamId, teamPlayers)
      teamList.append(myTeam)
      print str(myTeam), len(myTeam.getPlayers())
  
  # GET LEAGUE AVERAGES FROM TEAM AVERAGES
  n = len(teamList)
  lFt = 0.0
  lPf = 0.0
  lFta = 0.0
  lOrb = 0.0
  lTrb = 0.0
  lFga = 0.0
  lPts = 0.0
  lAst = 0.0
  lFg = 0.0
  lTov = 0.0
  for T in teamList:
    Ps = T.getPlayers()
    m = len(Ps) * 1.0
    lFt += sum([P.ft for P in Ps])/m
    lPf += sum([P.pf for P in Ps])/m
    lFta += sum([P.fta for P in Ps])/m
    lOrb += sum([P.orb for P in Ps])/m
    lTrb += sum([P.trb for P in Ps])/m
    lFga += sum([P.fga for P in Ps])/m
    lPts += sum([P.pts for P in Ps])/m
    lAst += sum([P.ast for P in Ps])/m
    lFg += sum([P.fg for P in Ps])/m
    lTov += sum([P.tov for P in Ps])/m
  L = league.League(ft=lFt/n, pf=lPf/n, fta=lFta/n, orb=lOrb/n, trb=lTrb/n, fga=lFga/n, pts=lPts/n, ast=lAst/n, fg=lFg/n, tov=lTov/n)
  print str(L)
  aperTotal = 0
  minutesTotal = 0
  for P in playerList:
    aper = P.getUPer(L)
    print P.name, aper
    print str(P)
    aperTotal += P.mp * aper
    minutesTotal += P.mp
  return aperTotal/minutesTotal

print getAverage()
