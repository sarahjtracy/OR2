import player
import league
import team
import positions

def getPERforPlayer(pid, tid, paceAd):
  P = player.Player(pid, tid, paceAd)
  L = league.season1314averages()
  per = P.getPER(L)
  print P.name, per, P.getIntangiblesScore()

def checkLebron():
  pid = 2544
  tid = 1610612748
  paceAd = 1.0325473383
  P = player.Player(pid, tid, paceAd)
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
  L = league.season1314averages()
  T = team.Team(tid, [], paceAd)
  print "Stats correct, PER =", P.getPER(L)
  print "Intangibles =", P.getIntangiblesScore()
  print "Age =", P.age

def checkDouble(val, act):
  err = 0.1
  assert(abs(val - act) < err)

checkLebron()
getPERforPlayer(101249, 1610612762, 1.0292378917)
getPERforPlayer(201142, 1610612760, 0.9840313245)
getPERforPlayer(201577, 1610612760, 1.0)
