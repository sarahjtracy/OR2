import league

def addToTeam():
  L = league.League()
  T = L.teams[0]
  for p in T.getPlayers():
    if (p.name == "Jeff Teague"):
       p.salary = 8000000
    elif (p.name == "Lou Williams"):
       p.salary = 5450000
    elif (p.name == "Paul Millsap"):
       p.salary = 9500000
    elif (p.name == "DeMarre Carroll"):
       p.salary = 2442455
    elif (p.name == "Pero Antic"):
       p.salary = 1250000
    elif (p.name == "John Jenkins"):
       p.salary = 1212920
    elif (p.name == "Gustavo Ayon"):
       p.salary = 1500000
    elif (p.name == "Al Horford"):
       p.salary = 12000000
    elif (p.name == "Dennis Schroder"):
       p.salary = 1690680
    elif (p.name == "Kyle Korver"):
       p.salary = 6253521
    elif (p.name == "Mike Muscala"):
       p.salary = 816482
    uPer = p.getUPer(L, teamAst=L.ast, teamFg=L.fg)
    if (p.isFreeAgent == False):
      print p.name
       #print p.playerId, uPer, p.position, p.salary
  print ("FREE AGENTS")
  for p in L.freeAgents:
    uPer = p.getUPer(L, teamAst=L.ast, teamFg=L.fg)
    #print p.playerId, uPer, p.position, p.salary
  

addToTeam()
