from pulp import *
import constants
import getPace
import player
import team
import nba_py
import freeAgents

def solveFreeAgency(teamId):

  # Get team pace from dictionary
  pace = constants.PACES.getPaceFromId(teamId)

  # Get Free Agents
  FA = freeAgents.FreeAgentsList()
  
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
  
  # Make player variables
  teamPlayerVars = []
  teamPositionVectors = []
  teamCosts = []
  positionVectors = []
  playerVariables = []
  costs = []
  values = []
  for P in playerList:
    name = "%d" %(int(P.playerId))
    var = LpVariable(name, 1, 1, cat="Integer")
    pv = getPositionVector(P.position)
    teamPlayerVars.append(var)
    teamCosts.append(P.salary)
    teamPositionVectors.append(pv)
  for P in FA.getAvailableFreeAgents():
    name = "%d" %(int(P.playerId))
    var = LpVariable(name, 0, 1, cat="Integer")
    playerVariables.append(var)
    costs.append(P.salary)
    values.append(P.getPER(constants.LEAGUE))
    pv = getPositionVector(P.position)
    positionVectors.append(pv)
  prob = LpProblem("FreeAgency", LpMaximize)
  n = len(playerVariables)
  
  # Objective function of indicator variables times value
  objective = [values[i] * playerVariables[i] for i in xrange(n)]
  prob += sum(objective)

  # Number of Player constraint
  prob += sum(playerVariables) + sum(teamPlayerVars) <= 15
  prob += sum(playerVariables) + sum(teamPlayerVars) >= 13

  # Salary Cap Constraint
  salaryConstraint = [costs[i] * playerVariables[i] for i in xrange(n)]
  currentSalaries = sum(teamCosts)
  prob += sum(salaryConstraint) + currentSalaries <= constants.SALARY_CAP
  #prob += sum(salaryConstraint) >= 0.9 * constants.SALARY_CAP
  
  # Players Per Position Constraint
  positions = []
  for i in xrange(5):
    positionsTotal = [positionVectors[j][i] * playerVariables[j] for j in xrange(n)]
    positionsTeam = [teamPositionVectors[j][i] * teamPlayerVars[j] for j in xrange(len(teamPlayerVars))]
    prob += sum(positionsTotal) + positionsTeam <= 3
    prob += sum(positionsTotal) + positionsTeam >= 1

  # Solve
  prob.solve()
  for indicator in playerVariables:
    if (value(indicator) == 1):
      print indicator

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
    pv = [0, 0, 0, 0, 0]
  return pv  
  
solveFreeAgency(1610612744)
