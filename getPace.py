class PaceDictionary(object):

  def __init__(self):
    F = open("pace.txt", 'r')
    self.paceDict = dict()
    for line in F:
      i = line.index('\t')
      j = line.index('\n')
      teamName = line[:i]
      teamPace = float(line[(i+1):j])
      if (teamName[:2] == "LA"):
        teamName = line[3:i]
      self.paceDict[teamName] = teamPace

  def getPace(self, teamCity, teamName):
    print "getPace ", teamCity, teamName
    if teamCity == "Los Angeles" or teamCity == "LA":
      key = teamName
    else:
      key = teamCity
    return self.paceDict[key]

  def __str__(self):
    dictStr = ""
    for key in list(paceDict.keys()):
      dictStr += "%s %.2f\n" %(key, paceDict[key])
    return dictStr
