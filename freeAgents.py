import nba_py
from nba_py import player
from nba_py import team
import constants
import re
import player
import getPace

NON_ALPHA_NUMERIC = '[^A-Za-z0-9]+'

class FreeAgentsList(object):
  def __init__(self):
    F = open("free_agents_salaries.txt", 'r')
    teamDict = getTeamAbbrDict()
    salaryDict = constants.SALARIES
    paceDict = getPace.PaceDictionary()
    self.freeAgentIds = set()
    self.availableFreeAgents = []
    for line in F:
      L = line.split('\t')
      name = str(L[0])
      i = name.index(' ')
      firstName = name[:i] #re.sub(NON_ALPHA_NUMERIC, '', name[:i])
      lastName = name[(i+1):] #re.sub(NON_ALPHA_NUMERIC, '', name[(i+1):])
      abbr = str(L[2])
      teamId = teamDict[abbr]
      salary = int(L[3])
      playerId = nba_py.player.get_player(firstName, last_name=lastName)
      self.freeAgentIds.add(playerId)
      if (name in salaryDict.keys()):
        (position, salary) = salaryDict[name]
        pace = paceDict.getPaceFromId(teamId)
        P = player.Player(playerId, teamId, constants.LEAGUE_PACE/pace, freeAgent=True)
        self.availableFreeAgents.append(P)
    print "%d out of %d free agents" %(len(self.availableFreeAgents), len(self.freeAgentIds))

  def isFreeAgent(self, playerId):
    return (playerId in self.freeAgentIds)

  def getAvailableFreeAgents(self):
    return self.availableFreeAgents

def getTeamAbbrDict():
  teamList = nba_py.team.TeamList().info()
  teamDict = dict()
  for T in teamList:
    abbr = T['ABBREVIATION']
    if (abbr != None):
      print abbr
      tid = T['TEAM_ID']
      teamDict[abbr] = tid
  return teamDict

F = FreeAgentsList()
