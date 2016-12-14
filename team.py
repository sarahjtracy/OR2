import nba_py
from nba_py import team
from player import Player
import constants

class Team(object):

   def __init__(self, teamId, players):
      self.teamId = teamId
      self.name = str(team.TeamSummary(teamId).info()[0]['TEAM_NAME'])
      self.players = players
      T = team.TeamYearOverYearSplits(teamId).by_year()[constants.SEASON_INDEX]
      self.ast = T['AST'] * 1.0
      self.fg = T['FGM'] * 1.0
      self.ft = T['FTM'] * 1.0
      self.pts = T['PTS'] * 1.0
      self.fga = T['FGA'] * 1.0
      self.orb = T['OREB'] * 1.0
      self.tov = T['TOV'] * 1.0
      self.fta = T['FTA'] * 1.0
      self.pf = T['PF'] * 1.0
      self.trb = T['REB'] * 1.0

   def __str__(self):
      return "%s: AST %.1f FGM %.1f FTM %.1f PTS %.1f FGA %.1f ORB %.1f TOV %.1f FTA %.1f PF %.1f TRB %.1f" % (self.name, self.ast, self.fg, self.ft, self.pts, self.fga, self.orb, self.tov, self.fta, self.pf, self.trb)

   def getPlayers(self):
      return self.players
