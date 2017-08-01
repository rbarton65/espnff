class Team(object):
    '''Teams are part of the league'''
    def __init__(self, data):
        self.team_id = self._try_except(data, 'teamId')
        self.team_abbrev = self._try_except(data, 'teamAbbrev')
        self.team_name = "%s %s" % (self._try_except(data, 'teamLocation'),
                                    self._try_except(data, 'teamNickname'))
        self.division_id = self._try_except(data['division'], 'divisionId')
        self.division_name = self._try_except(data['division'], 'divisionName')
        self.wins = self._try_except(data['record'], 'overallWins')
        self.losses = self._try_except(data['record'], 'overallLosses')
        self.points_for = self._try_except(data['record'], 'pointsFor')
        self.points_against = self._try_except(data['record'], 'pointsAgainst')
        self.owner = "%s %s" % (self._try_except(data['owners'][0], 'firstName'),
                                self._try_except(data['owners'][0], 'lastName'))
        self.schedule = []
        self.scores = []
        self.mov = []
        self._fetch_schedule(data)

    def __repr__(self):
        return 'Team(%s)' % (self.team_name, )

    def _try_except(self, data, key):
        '''Populate attributes'''
        try:
            return data[key]
        except:
            return "Unknown"

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

    def get_roster(self, week):
        '''Get roster for a given week'''
        roster = None
        return roster
