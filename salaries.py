import csv
import re

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
  return salaryDict
