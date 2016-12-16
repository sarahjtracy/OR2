import constants
import nba_py
from nba_py import team
import player
import team
import league
import getPace

# NOTE: This file has served various purposes to calculate average aPER values
#       as well as league average stats throughout our project. This file now
#       has several of these functions commented out. This file is not called
#       in the running of our current model, all of the results gained from it
#       have been stored as global variables in constants.py. Would not suggest
#       running this file as is, but remnants of the code used to calculate what
#       has been mentioned are here

def getAverage():
  pulledTeamList = nba_py.team.TeamList().info()
  playerList = []
  teamList = []
  paceDict = getPace.PaceDictionary()
  #print(len(teamList))
  ages = 0
  minplayed = 0
  # INITIALIZE TEAMS AND ROSTERS
  for T in pulledTeamList:
    abbr = T['ABBREVIATION']
    if (abbr != None): 
      #print abbr
      teamId = T['TEAM_ID']
      TSum = nba_py.team.TeamSummary(teamId).info()[0]
      pace = paceDict.getPace(str(TSum['TEAM_CITY']), str(TSum['TEAM_NAME']))
      R = nba_py.team.TeamCommonRoster(teamId, season=constants.SEASON).roster()
      teamPlayers = []
      for P in R:
        playerId = P['PLAYER_ID']
        myPlayer = player.Player(playerId, teamId, constants.LEAGUE_PACE/pace)
        teamPlayers.append(myPlayer)
        playerList.append(myPlayer)
        ages += myPlayer.mp * myPlayer.age
        minplayed += myPlayer.mp 
      myTeam = team.Team(teamId, teamPlayers, constants.LEAGUE_PACE/pace)
      teamList.append(myTeam)
      print str(myTeam), len(myTeam.getPlayers())
  print "AVG AGE ON COURT =", ages/minplayed
#  L = league.season1314averages()
 # print "WRITING"
  #outputFile = open("pers.txt", 'w')
  #for P in playerList:
   # strl = "%d, %s, %.1f\n" %(P.playerId, P.name, P.getPER(L))
    #outputFile.write(strl) 
  ## GET LEAGUE AVERAGES FROM TEAM AVERAGES
  #n = len(teamList)
  #lFt = 0.0
#  lPf = 0.0
 # lFta = 0.0
  #lOrb = 0.0
  #lTrb = 0.0
  #lFga = 0.0
  #lPts = 0.0
  #lAst = 0.0
  #lFg = 0.0
  #lTov = 0.0
  #for T in teamList:
  #  Ps = T.getPlayers()
  #  m = len(Ps) * 1.0
  #  lFt += sum([P.ft for P in Ps])/m
  #  lPf += sum([P.pf for P in Ps])/m
  #  lFta += sum([P.fta for P in Ps])/m
  #  lOrb += sum([P.orb for P in Ps])/m
  #  lTrb += sum([P.trb for P in Ps])/m
  #  lFga += sum([P.fga for P in Ps])/m
  #  lPts += sum([P.pts for P in Ps])/m
  #  lAst += sum([P.ast for P in Ps])/m
  #  lFg += sum([P.fg for P in Ps])/m
  #  lTov += sum([P.tov for P in Ps])/m
  #L = league.League(ft=lFt/n, pf=lPf/n, fta=lFta/n, orb=lOrb/n, trb=lTrb/n, fga=lFga/n, pts=lPts/n, ast=lAst/n, fg=lFg/n, tov=lTov/n)
  #print str(L)
  #aperTotal = 0
  #minutesTotal = 0
  #for P in playerList:
   # aper = P.getAPer(L)
   # print P.name, aper
    #print str(P)
   # aperTotal += P.mp * aper
    #minutesTotal += P.mp
  #return aperTotal/minutesTotal
  return 0
print getAverage()
