import requests

from .utils import (two_step_dominance,
                    power_points, )


class ESPNFFException(Exception):
    pass


class PrivateLeagueException(ESPNFFException):
    pass


class InvalidLeagueException(ESPNFFException):
    pass


class UnknownLeagueException(ESPNFFException):
    pass


class League(object):
    '''Creates a League instance for Public ESPN league'''
    def __init__(self, league_id, year):
        self.league_id = league_id
        self.year = year
        self.ENDPOINT = "http://games.espn.com/ffl/api/v2/"
        self.teams = []
        self._fetch_league()

    def __repr__(self):
        return 'League(%s, %s)' % (self.league_id, self.year, )

    def _fetch_league(self):
        params = {
            'leagueId': self.league_id,
            'seasonId': self.year
        }
        r = requests.get('%sleagueSettings' % (self.ENDPOINT, ), params=params)
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


class Team(object):
    '''Teams are part of the league'''
    def __init__(self, data):
        self.team_id = data['teamId']
        self.team_abbrev = data['teamAbbrev']
        self.team_name = "%s %s" % (data['teamLocation'], data['teamNickname'])
        self.division_id = data['division']['divisionId']
        self.division_name = data['division']['divisionName']
        self.wins = data['record']['overallWins']
        self.losses = data['record']['overallLosses']
        self.points_for = data['record']['pointsFor']
        self.points_against = data['record']['pointsAgainst']
        self.owner = "%s %s" % (data['owners'][0]['firstName'],
                                data['owners'][0]['lastName'])
        self.schedule = []
        self.scores = []
        self.mov = []
        self._fetch_schedule(data)

    def __repr__(self):
        return 'Team(%s)' % (self.team_name, )

    def _fetch_schedule(self, data):
        '''Fetch schedule and scores for team'''
        matchups = data['scheduleItems']

        for matchup in matchups:
            if not matchup['matchups'][0]['isBye']:
                if matchup['matchups'][0]['awayTeamId'] == self.team_id:
                    score = matchup['matchups'][0]['awayTeamScores'][0]
                    opponentId = matchup['matchups'][0]['homeTeamId']
                else:
                    score = matchup['matchups'][0]['homeTeamScores'][0]
                    opponentId = matchup['matchups'][0]['awayTeamId']
            else:
                score = matchup['matchups'][0]['homeTeamScores'][0]
                opponentId = matchup['matchups'][0]['homeTeamId']

            self.scores.append(score)
            self.schedule.append(opponentId)


class Settings(object):
    '''Creates Settings object'''
    def __init__(self, data):
        self.reg_season_count = data['leaguesettings']['finalRegularSeasonMatchupPeriodId']
        self.undroppable_list = data['leaguesettings']['usingUndroppableList']
        self.veto_votes_required = data['leaguesettings']['vetoVotesRequired']
        self.team_count = data['leaguesettings']['size']
        self.final_season_count = data['leaguesettings']['finalMatchupPeriodId']
        self.playoff_team_count = data['leaguesettings']['playoffTeamCount']
        self.id = data['leaguesettings']['id']
        self.keeper_count = data['leaguesettings']['futureKeeperCount']
        self.trade_deadline = data['leaguesettings']['tradeDeadline']
        self.name = data['leaguesettings']['name']
        self.status = data['metadata']['status']
        self.year = data['metadata']['seasonId']
        self.server_date = data['metadata']['serverDate']
        self._fetch_roster_settings(data)
        self._fetch_tie_rules(data)

    def __repr__(self):
        return 'Settings(%s)' % (self.name)

    def _fetch_roster_settings(self, data):
        '''Grabs roster settings'''
        roster_map = {
                      0: 'QB',
                      1: 'TQB',
                      2: 'RB',
                      3: 'RB/WR',
                      4: 'WR',
                      5: 'WR/TE',
                      6: 'TE',
                      7: 'OP',
                      8: 'DT',
                      9: 'DE',
                      10: 'LB',
                      11: 'DL',
                      12: 'CB',
                      13: 'S',
                      14: 'DB',
                      15: 'DP',
                      16: 'D/ST',
                      17: 'K',
                      18: 'P',
                      19: 'HC',
                      20: 'BE',
                      21: 'IR',
                      22: '',
                      23: 'RB/WR/TE'
                      }

        roster = data['leaguesettings']['slotCategoryItems']
        self.roster = {roster_map[i['slotCategoryId']]: i['num'] for i in roster
                       if i['num'] != 0}

    def _fetch_tie_rules(self, data):
        '''Grabs matchup and playoff seeding tie info'''
        tie_map = {
                   0: 'None',
                   1: 'Home Team Wins',
                   2: 'Most Bench Points',
                   3: 'Most QB Points',
                   4: 'Most RB Points'
                  }

        tie_id = data['leaguesettings']['tieRule']
        self.tie_rule = tie_map[tie_id]

        playoff_tie_map = {
                           0: 'Head to Head Record',
                           1: 'Total Points For',
                           2: 'Intra Division Record',
                           3: 'Total Points Against'
                          }
        playoff_id = data['leaguesettings']['playoffSeedingTieRuleRawStatId']
        self.playoff_seed_tie_rule = playoff_tie_map[playoff_id]


class Matchup(object):
    '''Creates Matchup instance'''
    def __init__(self, data):
        self.data = data
        self._fetch_matchup_info()

    def __repr__(self):
        return 'Matchup(%s, %s)' % (self.home_team, self.away_team, )

    def _fetch_matchup_info(self):
        '''Fetch info for matchup'''
        if self.data['teams'][0]['home'] and not self.data['bye']:
            self.home_team = self.data['teams'][0]['teamId']
            self.home_score = self.data['teams'][0]['score']
            self.away_team = self.data['teams'][1]['teamId']
            self.away_score = self.data['teams'][1]['score']
        elif self.data['teams'][0]['home'] and not self.data['bye']:
            self.home_team = self.data['teams'][1]['teamId']
            self.home_score = self.data['teams'][1]['score']
            self.away_team = self.data['teams'][0]['teamId']
            self.away_score = self.data['teams'][0]['score']
        else:
            self.home_team = self.data['teams'][0]['teamId']
            self.home_score = self.data['teams'][0]['score']
            self.away_team = None
            self.away_score = None
