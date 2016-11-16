from math import log10

class player(object):
  def __init__(self, name, tp, mp, ast, teamAst, teamFg, fg, 
               vop, tov, drb, fga, fta, ft, stl, orb, blk, pf,
               pts, trb, sa, df, lbr, cd, cs):
    self.name = name
    self.tp = tp # 3P
    self.mp = mp
    self.ast = ast
    self.teamAst = teamAst
    self.teamFg = teamFg
    self.fg = fg
    self.tov = tov
    self.fga = fga
    self.fta = fta
    self.ft = ft
    self.stl = stl
    self.orb = orb
    self.blk = blk
    self.pf = pf
    self.pts = pts
    self.trb = trb
    self.sa = sa             # screen assists
    self.df = df             # deflections
    self.lbr = lbr           # loose balls recovered
    self.cd = cd             # charges drawn
    self.cs = cs             # contested shots

  def getUPer(self):
    factor = (2/3) - (0.5 * (log10(self.ast)/log10(self.fg))) 
                      / (2 * log10(self.fg)/log10(self.ft))

    vop = log10(self.pts) / (log10(self.fga) - log10(self.orb) 
                             + log10(tov) + 0.44 * log10(self.fta))

    drb = (log10(self.trb) - log10(self.orb)) / log10(self.trb)

    uPer = (1 / self.mp) * [self.tp + (2/3) * self.ast 
            + (2 - factor * (self.teamAst / self.teamFg)) * self.fg
            + (self.ft * 0.5 * (1 + 1 - (self.teamAst / self.teamFg)) 
               + (2/3) * (self.teamAst/self.teamFg)) 
            - vop * self.tov
            - vop * drb * (self.fga - self.fg)
            - vop * 0.44 * (0.44 + (0.56 * drb)) * (self.fta - self.ft)
            + vop * (1 - self.drb) * (self.trb - self.orb)
            + vop * drb * self.orb
            + vop * self.stl
            + vop * drb * self.blk
            - self.pf * (log10(self.ft)/log10(self.pf) 
                         - 0.44 * (log10(self.fta)/log10(self.pf)) * vop) ]
    return uPer

  def getIntangiblesScore(self):
    intangibles = logCalc(self.sa) + logCalc(self.df) + logCalc(self.lbr) 
                  + logCalc(self.cd) + logCalc(cs)
    return intangibles 

def logCalc(x):
  return (x - log10(x))/log10(x)
