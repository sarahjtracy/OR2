from pulp import *
import constants
import getPace
import player
import team
import nba_py
import freeAgents

def solveFreeAgency(teamId):

  # Get team pace from dictionary
  teamSum = nba_py.team.TeamSummary(teamId).info()[0]
  pace = getPace.PaceDictionary().getPace(str(teamSum['TEAM_CITY']), str(teamSum['TEAM_NAME'])) 

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
  positionVectors = []
  playerVariables = []
  costs = []
  values = []
  for P in FA.getAvailableFreeAgents():
    name = "%d" %(int(P.playerId))
    var = LpVariable(name, 0, 1, cat=Integer)
    playerVariables.append(var)
    costs.append(P.salary)
    values.append(P.getPER(constants.LEAGUE))
    position = P.position
    if (position == positions.SF):
      pv = [1, 0, 0, 0, 0]
    elif (position == positions.PF):
      pv = [0, 1, 0, 0, 0]
    elif (position == positions.C):
      pv = [0, 0, 1, 0, 0]
    elif (position == positions.PG):
      pv = [0, 0, 0, 1, 0]
    else:
      pv = [0, 0, 0, 0, 0]
    positionVectors.append(pv)
  prob = LpProblem("FreeAgency", LpMaximize)
  n = len(playerVariables)
  
  # Objective function of indicator variables times value
  objective = [values[i] * playerVariables[i] for i in xrange(n)]
  prob += sum(objective)

  # Number of Player constraint
  prob += sum(playerVariables) <= 15
  prob += sum(playerVariables) >= 13

  # Salary Cap Constraint
  salaryConstraint = [costs[i] * playerVariables[i] for i in xrange(n)]
  prob += sum(salaryConstraint) <= constants.SALARY_CAP
  prob += sum(salaryConstraint) >= 0.9 * constants.SALARY_CAP
  
  # Players Per Position Constraint
  positions = []
  for i in xrange(5):
    positionsTotal = [positionVectors[j][i] * playerVariables[j] for j in xrange(n)]
    prob += sum(positionsTotal) <= 3
    prob += sum(positionsTotal) >= 1

  # Solve
  prob.solve()
  for indicator in playerVariables:
    if (value(indicator) == 1):
      print indicator
  
  
solveFreeAgency(1610612744)
