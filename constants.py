import league
import salaries
import getPace
SEASON = "2013-14"
SEASON_INDEX = 3
LEAGUE = league.season1314averages()
SALARY_CAP = 63000000
MIN_PLAYERS = 13
MAX_PLAYERS = 15
HUSTLE_URL = "http://stats.nba.com/stats/leaguehustlestatsplayer?PlayerID=2544&LastNGames=0&LeagueID=00&Month=0&OpponentTeamID=0&PORound=0&PaceAdjust=N&PerMode=PerGame&Period=0&PlusMinus=N&Rank=N&Season=2016-17&SeasonType=Regular+Season&Weight="
LEAGUE_PACE = 96.3367
PACES = getPace.PaceDictionary()
APER_AVG = 0.2856941022
SALARIES = salaries.getSalaries()
