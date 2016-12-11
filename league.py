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

def season1314():
  L = League(ft=17.8, pf=20.7, fta=23.6, orb=10.9, trb=42.7, 
             fga=83.0, pts=101.0, ast=22, fg=37.7, tov=14.6)
  return L
