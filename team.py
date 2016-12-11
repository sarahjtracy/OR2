import nba_py
from nba_py import team
from player import Player
import constants

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
      teamAst = 0
      teamFg = 0
      for i in xrange(len(self.players)):
        teamAst += self.players[i].ast
        teamFg += self.players[i].fg
      self.teamAst = teamAst
      self.teamFg = teamFg

   def initPlayers(self, teamId):
      players = []
      teamRoster = team.TeamCommonRoster(teamId, season=constants.SEASON).roster()
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
