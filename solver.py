from pulp import *
import constants
import getPace
import player
import team
import nba_py
import freeAgents

def solveFreeAgency(teamId, hustle=True):

  # Get team pace from dictionary
  pace = constants.PACES.getPaceFromId(teamId)
  print "Loading free agents..."
  # Get Free Agents
  FA = freeAgents.FreeAgentsList()
  
  print "Loading roster..."
  # Get players from nba_py team rosters and form team
  roster = nba_py.team.TeamCommonRoster(teamId, season=constants.SEASON).roster()
  playerList = []
  for playerDict in roster:
    playerId = playerDict['PLAYER_ID']
    if (not FA.isFreeAgent(playerId)):
      name = nba_py.player.PlayerSummary(playerId).headline_stats()[0]['PLAYER_NAME']
      if (name in constants.SALARIES.keys()):
        (position, salary) = constants.SALARIES[name]
      else:
        print name
        (position, salary) = (None, 0)
      P = player.Player(playerId, teamId, constants.LEAGUE_PACE/pace, position=position, salary=salary)
      print(P.name)
      playerList.append(P)
    else:
      print "FREE AGENT"
  T = team.Team(teamId, playerList, constants.LEAGUE_PACE/pace)
  
  # LP Maximization
  print "Starting LP Maximization..." 

  # Make player variables
  positionVectors = []
  playerVariables = []
  costs = []
  values = []
  valuesPlus = []
  positionCounts = [0, 0, 0, 0, 0]
  teamSalaries = [P.salary for P in playerList]
  for P in playerList:
    pv = getPositionVector(P.position)
    positionCounts = [positionCounts[i] + pv[i] for i in xrange(5)]
  print positionCounts
  k = 0
  for FP in FA.getAvailableFreeAgents():
    name = str(k)
    var = LpVariable(name, 0, 1, cat="Integer")
    playerVariables.append(var)
    costs.append(FP.salary)
    values.append(FP.getPER(constants.LEAGUE))
    valuesPlus.append(FP.getIntangiblesScore())
    pv = getPositionVector(FP.position)
    positionVectors.append(pv)
    k += 1

  prob = LpProblem("FreeAgency", LpMaximize)
  n = len(playerVariables)
  print n

  valuesTot = values
  if (hustle):
    valuesTot = [values[i]+valuesPlus[i] for i in xrange(n)]
  # Objective function of indicator variables times value
  objective = [valuesTot[i] * playerVariables[i] for i in xrange(n)]
  prob += sum(objective)

  # Number of Player constraint
  prob += sum(playerVariables) + len(playerList) <= 15
  prob += sum(playerVariables) + len(playerList) >= 13

  # Salary Cap Constraint
  salaryConstraint = [costs[i] * playerVariables[i] for i in xrange(n)]
  prob += sum(salaryConstraint) + sum(teamSalaries) <= constants.SALARY_CAP
  prob += sum(salaryConstraint) + sum(teamSalaries) >= 0.9 * constants.SALARY_CAP
  
  # Players Per Position Constraint
  positions = []
  for i in xrange(5):
    positionsTotal = [positionVectors[j][i] * playerVariables[j] for j in xrange(n)]
    prob += sum(positionsTotal) + positionCounts[i] <= 4
    prob += sum(positionsTotal) + positionCounts[i] >= 2

  # Solve
  prob.solve()
  salaryTot = 0
  perTot = 0
  intTot = 0
  print "CURRENT ROSTER\n--------------\n"
  for P in playerList:
    salaryTot += P.salary
    perTot += P.getPER(constants.LEAGUE)
    intTot += P.getIntangiblesScore()
    print P.name, P.salary, P.position
  print "--------------\n FREE AGENTS  \n--------------\n"
  for i in xrange(len(playerVariables)):
    indicator = playerVariables[i]
    P = FA.getAvailableFreeAgents()[i]
    if (value(indicator) == 1):
      perTot += P.getPER(constants.LEAGUE)
      salaryTot += P.salary
      intTot += P.getIntangiblesScore()
      print P.name, P.salary, P.position
  print "--------------"
  print "Total Salary =", salaryTot
  print "Total PER =", perTot
  print "Total Intangibles =", intTot

def getPositionVector(position):
  if (position == "SMALL FORWARD"):
    pv = [1, 0, 0, 0, 0]
  elif (position == "POWER FORWARD"):
    pv = [0, 1, 0, 0, 0]
  elif (position == "CENTER"):
    pv = [0, 0, 1, 0, 0]
  elif (position == "POINT GUARD"):
    pv = [0, 0, 0, 1, 0]
  else:
    pv = [0, 0, 0, 0, 1]
  return pv  
  
#solveFreeAgency(1610612759, hustle=False)
solveFreeAgency(1610612739, hustle=False)
