class League(object):
  def __init__(self, ft=0, pf=0, fta=0, orb=0, trb=0,
               fga=0, pts=0, ast=0, fg=0, tov=0):
    self.ft = ft
    self.pf = pf
    self.fta = fta
    self.orb = orb
    self.trb = trb
    self.fga = fga
    self.pts = pts
    self.ast = ast
    self.fg = fg
    self.tov = tov

  def __str__(self):
    return "FT %.1f PF %.1f FTA %.1f ORB %.1f TRB %.1f FGA %.1f PTS %.1f AST %.1f FG %.1f TOV %.1f" %(self.ft, self.pf, self.fta, self.orb, self.trb, self.fga, self.pts, self.ast, self.fg, self.tov)

def season1314():
  L = League(ft=17.8, pf=20.7, fta=23.6, orb=10.9, trb=42.7, 
             fga=83.0, pts=101.0, ast=22, fg=37.7, tov=14.6)
  return L

def season1314averages():
  L = League(ft=1.5, pf=1.9, fta=2.0, orb=1.0, trb=3.8, fga=7.2, pts=8.7, ast=1.9, fg=3.3, tov=1.2)
  return L
