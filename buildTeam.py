from pulp import *

def getFreeAgents():
   # Use NBA API or whatever to get the list of free agents
   return []

def algo(team):
   freeAgents = getFreeAgents();
   remainingBudget = team.budget - reduce(lambda x,y: x.cost + y.cost, team.players)
   
   ILP = LpProblem("build team", LpMaximize)
