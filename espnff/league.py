import requests

from .utils import (two_step_dominance,
                    power_points, )
from .team import Team
from .settings import Settings
from .matchup import Matchup
from .exception import (PrivateLeagueException,
                        InvalidLeagueException,
                        UnknownLeagueException, )


class League(object):
    '''Creates a League instance for Public ESPN league'''
    def __init__(self, league_id, year, espn_s2=None, swid=None):
        self.league_id = league_id
        self.year = year
        self.ENDPOINT = "http://games.espn.com/ffl/api/v2/"
        self.teams = []
        self.espn_s2 = espn_s2
        self.swid = swid
        self._fetch_league()

    def __repr__(self):
        return 'League(%s, %s)' % (self.league_id, self.year, )

    def _fetch_league(self):
        params = {
            'leagueId': self.league_id,
            'seasonId': self.year
        }

        cookies = None
        if self.espn_s2 and self.swid:
            cookies = {
                'espn_s2': self.espn_s2,
                'SWID': self.swid
            }

        r = requests.get('%sleagueSettings' % (self.ENDPOINT, ), params=params, cookies=cookies)
        self.status = r.status_code
        data = r.json()

        if self.status == 401:
            raise PrivateLeagueException(data['error'][0]['message'])

        elif self.status == 404:
            raise InvalidLeagueException(data['error'][0]['message'])

        elif self.status != 200:
            raise UnknownLeagueException('Unknown %s Error' % self.status)

        self._fetch_teams(data)
        self._fetch_settings(data)

    def _fetch_teams(self, data):
        '''Fetch teams in league'''
        teams = data['leaguesettings']['teams']

        for team in teams:
            self.teams.append(Team(teams[team]))

        # replace opponentIds in schedule with team instances
        for team in self.teams:
            for week, matchup in enumerate(team.schedule):
                for opponent in self.teams:
                    if matchup == opponent.team_id:
                        team.schedule[week] = opponent

        # calculate margin of victory
        for team in self.teams:
            for week, opponent in enumerate(team.schedule):
                mov = team.scores[week] - opponent.scores[week]
                team.mov.append(mov)

        # sort by team ID
        self.teams = sorted(self.teams, key=lambda x: x.team_id, reverse=False)

    def _fetch_settings(self, data):
        self.settings = Settings(data)

    def power_rankings(self, week):
        '''Return power rankings for any week'''

        # calculate win for every week
        win_matrix = []
        teams_sorted = sorted(self.teams, key=lambda x: x.team_id,
                              reverse=False)

        for team in teams_sorted:
            wins = [0]*32
            for mov, opponent in zip(team.mov[:week], team.schedule[:week]):
                opp = int(opponent.team_id)-1
                if mov > 0:
                    wins[opp] += 1
            win_matrix.append(wins)
        dominance_matrix = two_step_dominance(win_matrix)
        power_rank = power_points(dominance_matrix, teams_sorted, week)
        return power_rank

    def scoreboard(self, week=None):
        '''Returns list of matchups for a given week'''
        params = {
            'leagueId': self.league_id,
            'seasonId': self.year
        }
        if week is not None:
            params['matchupPeriodId'] = week

        r = requests.get('%sscoreboard' % (self.ENDPOINT, ), params=params)
        self.status = r.status_code
        data = r.json()

        if self.status == 401:
            raise PrivateLeagueException(data['error'][0]['message'])

        elif self.status == 404:
            raise InvalidLeagueException(data['error'][0]['message'])

        elif self.status != 200:
            raise UnknownLeagueException('Unknown %s Error' % self.status)

        matchups = data['scoreboard']['matchups']
        result = [Matchup(matchup) for matchup in matchups]

        for team in self.teams:
            for matchup in result:
                if matchup.home_team == team.team_id:
                    matchup.home_team = team
                if matchup.away_team == team.team_id:
                    matchup.away_team = team

        return result
