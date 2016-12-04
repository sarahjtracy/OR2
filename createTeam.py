from nba_py import player
from nba_py import team

def addToTeam(teamId):
  roster = team.TeamCommonRoster(teamId).roster()
  playerIds = []
  n = len(roster)
  for i in xrange(n):
    playerIds += [roster[i]['PLAYER_ID']]
  playerList = player.PlayerList().info()
  maxpts = 0
  maxpid = 0
  for i in xrange(len(playerList)-1):
    pid = playerList[i]['PERSON_ID']
    pts = player.PlayerSummary(pid).headline_stats()[0]['PTS']
    if (pts > maxpts):
      maxpts = pts
      maxpid = pid
  maxplayer = player.PlayerSummary(maxpid).headline_stats()[0]['PLAYER_NAME'] 
  print(str(maxplayer))
  print(maxpts)
  
addToTeam(1610612737)
