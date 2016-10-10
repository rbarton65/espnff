import requests

from .utils import two_step_dominance, power_points


class League(object):
    '''Creates a League instance for Public ESPN league'''
    def __init__(self, league_id, year):
        self.league_id = league_id
        self.year = year
        self.ENDPOINT = "http://games.espn.com/ffl/api/v2/"
        self.teams = []
        self._fetch_teams()

    def __repr__(self):
        return 'League %s, %s Season' % (self.league_id, self.year)

    def _fetch_teams(self):
        '''Fetch teams in league'''
        url = "%sleagueSettings?leagueId=%s&seasonId=%s"
        r = requests.get(url % (self.ENDPOINT, self.league_id, self.year))
        data = r.json()
        teams = data['leaguesettings']['teams']

        for team in teams:
            self.teams.append(Team(teams[team]))

        # replace opponentIds in schedule with team instances
        for team in self.teams:
            for week, matchup in enumerate(team.schedule):
                for opponent in self.teams:
                    if matchup == opponent.teamId:
                        team.schedule[week] = opponent

         # calculate margin of victory
        for team in self.teams:
            for week, opponent in enumerate(team.schedule):
                mov = team.scores[week] - opponent.scores[week]
                team.mov.append(mov)

    def power_rankings(self, week):
        '''Return power rankings for any week'''

        # calculate win for every week
        win_matrix = []
        teams_sorted = sorted(self.teams, key=lambda x: x.teamId, reverse=False)

        for team in teams_sorted:
            wins = [0]*32
            for mov,opponent in zip(team.mov[:week], team.schedule[:week]):
                opp = int(opponent.teamId)-1
                if mov > 0:
                    wins[opp]+=1
            win_matrix.append(wins)

        dominance_matrix = two_step_dominance(win_matrix)
        power_rank = power_points(dominance_matrix, teams_sorted, week)
        return sorted(power_rank.items(), key=lambda x: x[0], reverse=True)


class Team(object):
    '''Teams are part of the league'''
    def __init__(self, data):
        self.teamId = data['teamId']
        self.teamAbbrev = data['teamAbbrev']
        self.teamName = "%s %s" % (data['teamLocation'], data['teamNickname'])
        self.divisionId = data['division']['divisionId']
        self.divisionName = data['division']['divisionName']
        self.wins = data['record']['overallWins']
        self.losses = data['record']['overallLosses']
        self.pointsFor = data['record']['pointsFor']
        self.pointsAgainst = data['record']['pointsAgainst']
        self.owner = "%s %s" % (data['owners'][0]['firstName'], data['owners'][0]['lastName'])
        self.schedule = []
        self.scores = []
        self.mov = []
        self._fetch_schedule(data)

    def __repr__(self):
        return 'Team %s' % self.teamName

    def _fetch_schedule(self, data):
        '''Fetch schedule and scores for team'''
        matchups = data['scheduleItems']

        for matchup in matchups:
            if matchup['matchups'][0]['isBye'] == False:
                if matchup['matchups'][0]['awayTeamId'] == self.teamId:
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
