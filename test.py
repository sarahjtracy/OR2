import player
import league
import team

def checkLebron():
  pid = 2544
  tid = 1610612748
  P = player.Player(pid, tid)
  assert(P.isFreeAgent == False)
  assert(P.name == "LeBron James")
  checkDouble(P.tp, 1.5)
  checkDouble(P.mp, 37.7)
  checkDouble(P.ast, 6.3)
  checkDouble(P.fg, 10)
  checkDouble(P.tov, 3.5)
  checkDouble(P.fga, 17.6)
  checkDouble(P.fta, 7.6) 
  checkDouble(P.ft, 5.7)
  checkDouble(P.stl, 1.6)
  checkDouble(P.orb, 1.1)
  checkDouble(P.blk, 0.3)
  checkDouble(P.pf, 1.6)
  checkDouble(P.pts, 27.1)
  checkDouble(P.trb, 6.9)
  checkDouble(P.drb, 5.9)
  checkDouble(P.sa, 0)
  checkDouble(P.df, 0)
  checkDouble(P.lbr,0)
  checkDouble(P.cd, 0)
  checkDouble(P.cost, 0)
  assert(P.position == "Forward")
  checkDouble(P.salary, 0) 
  L = league.season1314averages()
  T = team.Team(tid, [])
  print "Stats correct, PER = ", P.getUPer(L)
  print str(P)
  print str(T)
  print str(L)

def checkDouble(val, act):
  err = 0.1
  assert(abs(val - act) < err)

checkLebron()
