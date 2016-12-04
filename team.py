import nba_py
from nba_py import team

class Team(object):

   def __init__(self, teamId, budget, minPlayers, maxPlayers, minPlayerPerPos, maxPlayerPerPos):
      self.teamId = teamId
      self.name = str(team.TeamSummary(teamId).info()[0]['TEAM_NAME'])
      self.players = self.initPlayers(teamId)
      self.budget = budget
      self.minPlayers = minPlayers
      self.maxPlayers = maxPlayers
      self.minPlayerPerPos = minPlayerPerPos
      self.maxPlayerPerPos = maxPlayerPerPos

   def initPlayers(self, teamId):
      players = []
      teamRoster = team.TeamCommonRoster(teamId).roster()
      for i in xrange(len(teamRoster)):
        playerId = teamRoster[i]['PLAYER_ID']
        players += [Player(playerId)]
      return players

   def getPlayers(self):
      return self.players

   def getBudget(self):
      return self.budget

   def getMinPlayers(self):
      return self.getMinPlayers

   def getMaxPlayers(self):
      return self.getMaxPlayers

   def getMinPlayerPos(self):
      return self.getMinPlayerPos

   def getMaxPlayerPos(self):
      return self.getMaxPlayerPos

atl = Team(1610612737, 0, 0, 0, 0, 0)
print(atl.getPlayers()) 
