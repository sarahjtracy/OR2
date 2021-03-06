import league
import salaries
import getPace
import hustle_avg

# Various constants to be used throughout the model


SEASON = "2013-14"
SEASON_INDEX = 3
LEAGUE = league.season1314averages()
SALARY_CAP = 63000000
MIN_PLAYERS = 13
MAX_PLAYERS = 15
HUSTLE_URL = 'http://stats.nba.com/stats/leaguehustlestatsplayer?PlayerID=2544&LastNGames=0&LeagueID=00&Month=0&OpponentTeamID=0&PORound=0&PaceAdjust=N&PerMode=PerGame&Period=0&PlusMinus=N&Rank=N&Season=2016-17&SeasonType=Regular+Season&Weight='
LEAGUE_PACE = 96.3367
PACES = getPace.PaceDictionary()
APER_AVG = 0.2856941022
SALARIES = salaries.getSalaries()
HUSTLE = hustle_avg.Hustle().getHustleDict()
AVG_SA = .78
AVG_DF = 1.255
AVG_LBR = .4033
AVG_CD = 0.04911
AVG_CS = 4.184
AVG_AGE = 30.0901702666
HUSTLE_AVG = (AVG_SA, AVG_DF, AVG_LBR, AVG_CD, AVG_CS)
