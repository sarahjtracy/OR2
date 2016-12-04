import nba_py
from nba_py import player


class Player(object):
  def __init__(self, playerId):
    self.playerId = playerId
    summary = player.PlayerSummary(playerId)
    hs = summary.headline_stats()[0]
    info = summary.info()[0]
    pc = player.PlayerCareer(playerId).regular_season_career_totals()[0]
    self.name = str(headlineStats['PLAYER_NAME'])
    self.tp = 0 #@TODO                # three points made
    self.mp = pc['MIN']               # minutes played
    self.ast = hs['AST']              # assists
    self.teamAst = 0 #@TODO           # team assists
    self.teamFg = 0 #@TODO            # team field goals
    self.fg = #@TODO                  # field goals
    self.tov = pc['TOV']              # turnovers
    self.fga = pc['FGA']              # field goals attempted
    self.fta = pc['FTA']              # free throws attempted
    self.ft = pc['FTM']               # free throws made
    self.stl = pc['STL']              # steals
    self.orb = pc['OREB']             # offensive rebounds
    self.blk = pc['BLK']              # blocks
    self.pf = pc['PF']                # personal fouls
    self.pts = hs['PTS']              # points
    self.trb = hs['REB']              # total rebounds
    self.sa = 0 #@TODO                # screen assists
    self.df = 0 #@TODO                # deflections
    self.lbr = 0 #@TODO               # loose balls recovered
    self.cd = 0 #@TODO                # charges drawn
    self.cs = 0 #@TODO                # contested shots
    self.cost = 0 #@TODO              # cost of player
    self.pos = str(info['POSITION'])  # position of player

  def getUPer(self, league, team):
    factor = (2/3) - (0.5 * league.ast/league.fg) \
                      / (2 * league.fg/league.ft)

    vop = league.pts / (league.fga - league.orb \
                             + league.tov + 0.44 * league.fta)

    drb = (league.trb - league.orb) / league.trb

    uPer = (1 / self.mp) * [self.tp + (2/3) * self.ast \
            + (2 - factor * (self.teamAst / self.teamFg)) * self.fg \
            + (self.ft * 0.5 * (1 + (1 - (self.teamAst / self.teamFg)) \
               + (2/3) * (self.teamAst / self.teamFg) \
            - vop * self.tov \
            - vop * drb * (self.fga - self.fg) \
            - vop * 0.44 * (0.44 + (0.56 * drb)) * (self.fta - self.ft) \
            + vop * (1 - self.drb) * (self.trb - self.orb) \
            + vop * drb * self.orb \
            + vop * self.stl \
            + vop * drb * self.blk \
            - self.pf * (league.ft/league.pf \
                         - 0.44 * (league.fta/league.pf * vop) ]
    return uPer

  def getIntangiblesScore(self, league):
    intangibles = self.leagueComparison(self.sa, league.sa)
                + self.leagueComparison(self.df, league.df)
                + self.leagueComparison(self.lbr, league.lbr)
                + self.leagueComparison(self.cd, league.cd)
                + self.leagueComparison(self.cs, league.cs)
    return intangibles 

  def leagueComparison(self, stat, leagueStat):
    return (stat - leagueStat) / leagueStat

  def getCost(self):
    return self.cost

  def getPos(self):
    return self.pos
