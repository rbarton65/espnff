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
        try:
            self.trade_deadline = data['leaguesettings']['tradeDeadline']
        except:
            self.trade_deadline = 'Unknown'
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

        try:
            self.tie_rule = tie_map[tie_id]
        except:
            self.tie_rule = 'Unknown'

        playoff_tie_map = {
                           -1: 'Head to Head Record',
                           0: 'Total Points For',
                           1: 'Intra Division Record',
                           2: 'Total Points Against'
                          }

        playoff_id = data['leaguesettings']['playoffSeedingTieRuleRawStatId']

        try:
            self.playoff_seed_tie_rule = playoff_tie_map[playoff_id]
        except:
            self.playoff_seed_tie_rule = 'Unknown'