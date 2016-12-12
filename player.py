import constants
import nba_py
from nba_py import player
from nba_py import team

class Player(object):
  def __init__(self, playerId, teamId, freeAgent=False):
    self.playerId = playerId
    self.teamId = teamId
    summary = player.PlayerSummary(playerId)
    info = summary.info()[0]
    hs = player.PlayerSummary(playerId).headline_stats()[0]
    years = player.PlayerYearOverYearSplits(playerId).by_year()
    i = 0
    while(str(years[i]['GROUP_VALUE']) != constants.SEASON and (i < len(years) - 1)):
      i += 1
    if (i == len(years)):
      pc = years[len(years)-1]
    else:
      pc = years[i]
    self.isFreeAgent = freeAgent
    self.name = str(hs['PLAYER_NAME'])
    self.tp = pc['FG3M'] #@TODO check  # three points made
    self.mp = pc['MIN']               # minutes played
    self.ast = pc['AST']              # assists
    self.fg = pc['FGM']               # field goals
    self.tov = pc['TOV']              # turnovers
    self.fga = pc['FGA']              # field goals attempted
    self.fta = pc['FTA']              # free throws attempted
    self.ft = pc['FTM']               # free throws made
    self.stl = pc['STL']              # steals
    self.orb = pc['OREB']             # offensive rebounds
    self.blk = pc['BLK']              # blocks
    self.pf = pc['PF']                # personal fouls
    self.pts = pc['PTS']              # points
    self.trb = pc['REB']              # total rebounds
    self.drb = pc['DREB']             # defensive rebounds
    self.sa = 0 #@TODO                # screen assists
    self.df = 0 #@TODO                # deflections
    self.lbr = 0 #@TODO               # loose balls recovered
    self.cd = 0 #@TODO                # charges drawn
    self.cs = 0 #@TODO                # contested shots
    self.cost = 0 #@TODO              # cost of player
    self.position = str(info['POSITION'])  # position of player
    self.salary = 0
 
  def getUPer(self):
    league = constants.LEAGUE
    T = team.TeamYearOverYearSplits(self.teamId).by_year()[constants.SEASON_INDEX]
    teamAst = T['AST']
    teamFg = T['FGM']
    factor = (2/3) - (0.5 * league.ast/league.fg) \
                      / (2 * league.fg/league.ft)
    vop = league.pts / (league.fga - league.orb \
                             + league.tov + 0.44 * league.fta)
    drb = (league.trb - league.orb) / league.trb
    uPer = (1 / self.mp) * ( self.tp
        + (2/3) * self.ast
        + (2 - factor * (teamAst / teamFg)) * teamFg
        + (self.ft * 0.5 * (1 + (1 - (teamAst / teamFg)) + (2/3) * (teamAst / teamFg)))
        - vop * self.tov
        - vop * drb * (self.fga - self.fg)
        - vop * 0.44 * (0.44 + (0.56 * drb)) * (self.fta - self.ft)
        + vop * (1 - drb) * (self.trb - self.orb)
        + vop * drb * self.orb
        + vop * self.stl
        + vop * drb * self.blk
        - self.pf * ((league.ft / league.pf) - 0.44 * (league.fta / league.pf) * vop))
    return uPer 

  def isFreeAgent(self):
    return self.isFreeAgent

  def setFreeAgent(self):
    self.freeAgent = True

  def getIntangiblesScore(self, league):
    intangibles = self.leagueComparison(self.sa, league.sa) \
                + self.leagueComparison(self.df, league.df) \
                + self.leagueComparison(self.lbr, league.lbr) \
                + self.leagueComparison(self.cd, league.cd) \
                + self.leagueComparison(self.cs, league.cs)
    return intangibles 

  def leagueComparison(self, stat, leagueStat):
    return (stat - leagueStat) / leagueStat

  def setSalary(self, salary):
    self.salary = salary

  def getCost(self):
    return self.cost

  def getPos(self):
    return self.position
