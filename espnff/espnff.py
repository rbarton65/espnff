import requests


class League(object):
    '''Creates a League instance for Public ESPN league'''
    def __init__(self, league_id, year):
        self.league_id = league_id
        self.year = year
        self.ENDPOINT = "http://games.espn.com/ffl/api/v2/"
        self.members = []
        self._fetch_members()

    def _fetch_members(self):
        '''Fetch members in league'''
        url = "%sleagueSettings?leagueId=%s&seasonId=%s"
        r = requests.get(url % (self.ENDPOINT, self.league_id, self.year))
        data = r.json()
        teams = data['leaguesettings']['teams']

        for team in teams:
            self.members.append(Member(teams[team]))

        # replace opponentIds in schedule with member instances
        for member in self.members:
            for week, matchup in enumerate(member.schedule):
                for opponent in self.members:
                    if matchup == opponent.teamId:
                        member.schedule[week] = opponent
        
         # calculate margin of victory
        for member in self.members:
            for week, opponent in enumerate(member.schedule):
                mov = member.scores[week] - opponent.scores[week]
                member.mov.append(mov)
    
    def power_rankings(self, week):
        '''Return power rankings for any week'''
        return
       
        


class Member(object):
    '''Members are part of the league'''
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

league = League(288077, 2016)

for team in league.members:
    print(team.teamName)
    print(team.scores)
    print(team.mov)
    print(team.wins)