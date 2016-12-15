import nba_py
from nba_py import team

class PaceDictionary(object):

  def __init__(self):
    F = open("pace.txt", 'r')
    self.paceDict = dict()
    self.teamIdDict = dict()
    for line in F:
      i = line.index('\t')
      j = line.index('\n')
      teamName = line[:i]
      teamPace = float(line[(i+1):j])
      if (teamName[:2] == "LA"):
        teamName = line[3:i]
      self.paceDict[teamName] = teamPace

  def getPace(self, teamCity, teamName):
    if teamCity == "Los Angeles" or teamCity == "LA":
      key = teamName
    else:
      key = teamCity
    return self.paceDict[key]

  def getPaceFromId(self, teamId):
    if (teamId in self.teamIdDict):
      (city, name) = self.teamIdDict[teamId]
    else:
      tsum = team.TeamSummary(teamId).info()[0]
      city = tsum['TEAM_CITY']
      name = tsum['TEAM_NAME']
      self.teamIdDict[teamId] = (city, name)
    return self.getPace(city, name)

  def __str__(self):
    dictStr = ""
    for key in list(paceDict.keys()):
      dictStr += "%s %.2f\n" %(key, paceDict[key])
    return dictStr
