import nba_py
from nba_py import player
import constants
import re

NON_ALPHA_NUMERIC = '[^A-Za-z0-9]+'

def getFreeAgents():
  F = open("free_agents.txt", 'r')
  salaryDict = dict()
  teamDict = getTeamAbbrDict()
  for line in F:
    i = line.index(' ')
    firstName = re.sub(NON_ALPHA_NUMERIC, '', line[:i])
    j = line.index('\t')
    lastName = re.sub(NON_ALPHA_NUMERIC, '', line[(i+1):j])
    k = line.index('\n')
    salary = int(line[(j+1):k])
    #print firstName, lastName
    try:
      playerId = player.get_player(firstName, last_name=lastName)
      salaryDict[playerId] = salary
    except player.PlayerNotFoundException:
      print(firstName + " " + lastName + " not found :(")
  return salaryDict

def getTeamAbbrDict():
  teamList = nba_py.team.TeamList().info()
  teamDict = dict()
  for T in teamList:
    abbr = T['ABBREVIATION']
    if (abbr != None):
      tid = T['TEAM_ID']
      teamDict[abbr] = tid
  return teamDict
