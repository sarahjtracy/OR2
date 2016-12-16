import csv
import re

# method to read the 2014 salary data from the csv
# into a dictionary

NON_NUMERIC = '[^0-9]+'

def getSalaries():
  salaryDict = dict()
  with open('2014_2015_Salaries.csv', 'rb') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for row in reader:
      if (len(row) < 4):
        print row
      namePos = str(row[2])
      i = namePos.index('\n')
      name = namePos[:i]
      position = namePos[(i+1):]
      salary = int(re.sub(NON_NUMERIC, '', row[3]))
      salaryDict[name] = (position, salary)

  # NOTE: As mentioned in solver.py, some salary data is missing
  # for players with complications during the 2014-15 season. 
  # Once it is noted that a player has a missing salary, insert their
  # salary and position in the manner shown below:

  salaryDict["Carrick Felix"] = ("SMALL GUARD", 510000)
  return salaryDict
