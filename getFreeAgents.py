import nba_py
from nba_py import player
import constants
import re

NON_ALPHA_NUMERIC = '[^A-Za-z0-9]+'

def getFreeAgents():
  F = open("free_agents.txt", 'r')
  salaryDict = dict()
  for line in F:
    i = line.index(' ')
    firstName = re.sub(NON_ALPHA_NUMERIC, '', line[:i])
    j = line.index('\t')
    lastName = re.sub(NON_ALPHA_NUMERIC, '', line[(i+1):j])
    k = line.index('\n')
    salary = int(line[(j+1):k])
    try:
      playerId = player.get_player(firstName, last_name=lastName)
      salaryDict[playerId] = salary
    except player.PlayerNotFoundException:
      print(firstName + " " + lastName + " not found :(")
  return salaryDict
