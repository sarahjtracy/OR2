import nba_py
from nba_py import team
from nba_py import player
import constants

class League(object):
  def __init__(self, season=constants.SEASON):
    teamList = team.TeamList().info()
    teams = []
    players = []
    for i in xrange(len(teamList)):
      teamId = teamList[i]['TEAM_ID']
      team = Team(teamId, constants.SALARY_CAP, constants.MIN_PLAYERS, constants.MAX_PLAYERS, 0, 8)
      teams += [team]
      players += team.getPlayers()
    self.teams = teams
    self.ft = 0
    self.pf = 0
    self.fta = 0
    self.orb = 0
    self.trb = 0
    self.fga = 0
    self.pts = 0
    self.ast = 0
    self.fg = 0
    for i in xrange(len(players)):
      self.ft += player.ft
      self.pf += player.pf
      self.fta += player.fta
      self.orb += player.orb
      self.trb += player.trb
      self.fga += player.fga
      self.pts += player.pts
      self.ast += player.ast
      self.fg += player.fg
