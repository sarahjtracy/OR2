from pulp import *
import constants
import getPace
import player
import team
import nba_py
import freeAgents

# This is the method solving the free agency problem for a given team
#
# To run on a given team, you must provide the Team ID as given on 
# stats.nba.com. Find the team ID by searching for a team on stats.nba.com.
# Once you are on the stats page for a specific team, the Team ID will 
# appear in the URL.
#
# Examples are provided at the bottom. To run this file on a team, change
# the line at the bottom to solveFreeAgency(teamId). Then run in terminal
# with:
#    python solver.py
#
# You can toggle use of hustle stats with hustle=True
#
# NOTE: Salary data is pulled from 2014-15 salaries. Some players on teams
# may not be free agents but end up leaving during the 2014 season, or 
# having some other complication, and these players do not have salary data
# available. The model will print players for which salary data is required 
# and set their current salary to 0. To update this, you must place their salaries
# in salaries.py in the manner described there. 

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
        print "Salary and position data need for:", name
        (position, salary) = (None, 0)
      P = player.Player(playerId, teamId, constants.LEAGUE_PACE/pace, position=position, salary=salary)
      playerList.append(P)
  T = team.Team(teamId, playerList, constants.LEAGUE_PACE/pace)

  # Determine whether team is rebuilding or playoff contender
  rebuilding = False
  if (T.winPercentage < .5):
    print "Acting as a REBUILDING YEAR"
    rebuilding = True

  # LP Maximization
  print "Starting LP Maximization..." 

  # Make player variables
  positionVectors = []
  playerVariables = []
  costs = []
  values = []
  valuesPlus = []
  ageDiff = []
  maxPerPosition = [0, 0, 0, 0, 0]
  positionCounts = [0, 0, 0, 0, 0]
  teamSalaries = [P.salary for P in playerList]
  for P in playerList:
    pv = getPositionVector(P.position)
    val = P.getPER(constants.LEAGUE)
    if (hustle): val += P.getIntangiblesScore()
    if (rebuilding): val += 0.5 * (constants.AVG_AGE - P.age)
    positionIndex = pv.index(1)
    if (val > maxPerPosition[positionIndex]):
      maxPerPosition[positionIndex] = val
    positionCounts = [positionCounts[i] + pv[i] for i in xrange(5)]
  
  k = 0
  for FP in FA.getAvailableFreeAgents():
    name = str(k)
    var = LpVariable(name, 0, 1, cat="Integer")
    playerVariables.append(var)
    costs.append(FP.salary)
    values.append(FP.getPER(constants.LEAGUE))
    ageDiff.append(0.5 * (constants.AVG_AGE - FP.age))
    valuesPlus.append(FP.getIntangiblesScore())
    pv = getPositionVector(FP.position)
    positionVectors.append(pv)
    k += 1

  n = len(playerVariables)
  valuesTot = values
  if (hustle):
    valuesTot = [values[i]+valuesPlus[i] for i in xrange(n)]
  valuesTotPlus = valuesTot
  if (rebuilding):
    valuesTotPlus = [values[i] + ageDiff[i] for i in xrange(n)]
  for i in xrange(n):
    positionIndex = positionVectors[i].index(1)
    if (valuesTotPlus[i] > maxPerPosition[positionIndex]):
      valuesTotPlus[i] *= 1.5
  
  solution = solveLP(values, costs, playerVariables, positionVectors, sum(teamSalaries), positionCounts, n)
  
  # PRINT RESULTS
  salaryTot = 0
  perTot = 0
  intTot = 0
  print "--------------\nCURRENT ROSTER\n--------------\n"
  for P in playerList:
    salaryTot += P.salary
    perTot += P.getPER(constants.LEAGUE)
    intTot += P.getIntangiblesScore()
    print P.name, P.salary, P.position
  print "--------------\n FREE AGENTS  \n--------------\n"
  for i in xrange(len(playerVariables)):
    indicator = solution[i]
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

def solveLP(values, costs, variables, positionVectors, costConstraint, positionConstraints, n):
  prob = LpProblem("FreeAgency", LpMaximize)

  # Objective function of indicator variables times value
  objective = [values[i] * variables[i] for i in xrange(n)]
  prob += sum(objective)

  # Number of Player constraint
  prob += sum(variables) + sum(positionConstraints) <= 15
  prob += sum(variables) + sum(positionConstraints) >= 13

  # Salary Cap Constraint
  salaryConstraint = [costs[i] * variables[i] for i in xrange(n)]
  prob += sum(salaryConstraint) + costConstraint <= constants.SALARY_CAP
  prob += sum(salaryConstraint) + costConstraint >= 0.9 * constants.SALARY_CAP
  
  # Players Per Position Constraint
  for i in xrange(5):
    positionsTotal = [positionVectors[j][i] * variables[j] for j in xrange(n)]
    prob += sum(positionsTotal) + positionConstraints[i] <= 4
    prob += sum(positionsTotal) + positionConstraints[i] >= 2

  # Solve
  prob.solve()
  return variables

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
  
#solveFreeAgency(1610612759, hustle=True) # UNCOMMENT FOR SAN ANTONIO SPURS
solveFreeAgency(1610612739, hustle=True) # UNCOMMENT FOR CLEVELAND CAVALIERS
