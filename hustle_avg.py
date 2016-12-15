import json

class Hustle(object):
  
  def __init__(self):
    self.hustleDict = dict()
    with open('hustle.json', 'r') as f:
      d = json.loads(f.read())['resultSets'][0]['rowSet']
 
      for P in d:
        playerId = P[0]
        sa = P[12]
        df = P[10]
        lbr = P[11]
        cd = P[9]
        cs = P[6]
        self.hustleDict[playerId] = (sa, df, lbr, cd, cs)
      n = len(d)
      avg_sa = sum(map(lambda x: 0 if x[12] is None else x[12], d))/n
      avg_df = sum(map(lambda x: 0 if x[10] is None else x[10], d))/n
      avg_lbr = sum(map(lambda x: 0 if x[11] is None else x[11], d))/n
      avg_cd = sum(map(lambda x: 0 if x[9] is None else x[9], d))/n
      avg_cs = sum(map(lambda x: 0 if x[6] is None else x[6], d))/n
      #print avg_sa, avg_df, avg_lbr, avg_cd, avg_cs

  def getHustleDict(self):
    return self.hustleDict
      #print "SA %.1f DF %.1f LBR %.1f CD %.1f OT %.1f" %(avg_sa, avg_df, avg_lbr, avg_cd, avg_cs) 

H = Hustle()

