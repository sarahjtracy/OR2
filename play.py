import nba_py
from nba_py import team
import constants

teamList = team.TeamList().info()
for T in teamList:
  print str(T['ABBREVIATION'])
