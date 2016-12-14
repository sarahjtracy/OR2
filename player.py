import constants
import requests
import json
import nba_py
from nba_py import player
from nba_py import team

class Player(object):

  def __init__(self, playerId, teamId, paceAdjustment, freeAgent=False):
    self.playerId = playerId
    self.teamId = teamId
    self.paceAdjustment = paceAdjustment
    summary = player.PlayerSummary(playerId)
    info = summary.info()[0]
    header = player.PlayerSummary(playerId).headline_stats()[0]
    years = player.PlayerYearOverYearSplits(playerId).by_year()
    i = 0
    while(str(years[i]['GROUP_VALUE']) != constants.SEASON and (i < len(years) - 1)):
      i += 1
    if (i == len(years)):
      pc = years[len(years)-1]
    else:
      pc = years[i]
    
    # Request hustle stats
    #r = requests.get(constants.HUSTLE_URL)
    #d = json.loads(r.content)['resultSets'][0]['rowSet']
    #hs = filter(lambda x: x[0] == playerId, d)[0]
    
    self.isFreeAgent = freeAgent
    self.name = str(header['PLAYER_NAME'])
    #self.sa = hs[12]                  # screen assists
    #self.df = hs[10]                  # deflections
    #self.lbr = hs[11]                 # loose balls recovered
    #self.cd = hs[9]                   # charges drawn
    #self.cs = hs[6]                   # contested shots
    self.tp = pc['FG3M'] * 1.0             # three points made
    self.mp = pc['MIN']  * 1.0             # minutes played
    self.ast = pc['AST'] * 1.0             # assists
    self.fg = pc['FGM'] * 1.0              # field goals
    self.tov = pc['TOV'] * 1.0             # turnovers
    self.fga = pc['FGA'] * 1.0             # field goals attempted
    self.fta = pc['FTA'] * 1.0             # free throws attempted
    self.ft = pc['FTM'] * 1.0              # free throws made
    self.stl = pc['STL'] * 1.0             # steals
    self.orb = pc['OREB'] * 1.0            # offensive rebounds
    self.blk = pc['BLK'] * 1.0             # blocks
    self.pf = pc['PF'] * 1.0               # personal fouls
    self.pts = pc['PTS'] * 1.0             # points
    self.trb = pc['REB'] * 1.0             # total rebounds
    self.drb = pc['DREB'] * 1.0            # defensive rebounds
    self.cost = 0 #@TODO              # cost of player
    self.position = str(info['POSITION'])  # position of player
    self.salary = 0
 
  def __str__(self):
    return "MIN %.1f PTS %.1f FGM %.1f FGA %.1f 3PM %.1f FTM %.1f FTA %.1f OREB %.1f DREB %.1f REB %.1f AST %.1f TOV %.1f STL %.1f BLK %.1f PF %.1f" %(self.mp, self.pts, self.fg, self.fga, self.tp, self.ft, self.fta, self.orb, self.drb, self.trb, self.ast, self.tov, self.stl, self.blk, self.pf)

  def getPER(self, league):
    T = team.TeamYearOverYearSplits(self.teamId).by_year()[constants.SEASON_INDEX]
    teamAst = T['AST'] * 1.0
    teamFg = T['FGM'] * 1.0
    factor = (2.0/3.0) - (0.5 * league.ast/league.fg) \
                      / (2.0 * league.fg/league.ft)
    vop = league.pts / (league.fga - league.orb \
                             + league.tov + 0.44 * league.fta)
    drbp = (league.trb - league.orb) / league.trb
    uPer = (1.0 / self.mp) * ( self.tp
        + (2.0/3.0) * self.ast
        + (2.0 - factor * (teamAst / teamFg)) * self.fg
        + (self.ft * 0.5 * (1.0 + (1.0 - (teamAst / teamFg)) + (2.0/3.0) * (teamAst / teamFg)))
        - vop * self.tov
        - vop * drbp * (self.fga - self.fg)
        - vop * 0.44 * (0.44 + (0.56 * drbp)) * (self.fta - self.ft)
        + vop * (1.0 - drbp) * (self.trb - self.orb)
        + vop * drbp * self.orb
        + vop * self.stl
        + vop * drbp * self.blk
        - self.pf * ((league.ft / league.pf) - 0.44 * (league.fta / league.pf) * vop))
    return (uPer * self.paceAdjustment) * (15.0/constants.APER_AVG)

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
