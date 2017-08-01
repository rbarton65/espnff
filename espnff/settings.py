class Settings(object):
    '''Creates Settings object'''
    def __init__(self, data):
        self.reg_season_count = self._try_except(data['leaguesettings'], 'finalRegularSeasonMatchupPeriodId')
        self.undroppable_list = self._try_except(data['leaguesettings'], 'usingUndroppableList')
        self.veto_votes_required = self._try_except(data['leaguesettings'], 'vetoVotesRequired')
        self.team_count = self._try_except(data['leaguesettings'], 'size')
        self.final_season_count = self._try_except(data['leaguesettings'], 'finalMatchupPeriodId')
        self.playoff_team_count = self._try_except(data['leaguesettings'], 'playoffTeamCount')
        self.id = self._try_except(data['leaguesettings'], 'id')
        self.keeper_count = self._try_except(data['leaguesettings'], 'futureKeeperCount')
        self.trade_deadline = self._try_except(data['leaguesettings'], 'tradeDeadline')
        self.name = self._try_except(data['leaguesettings'], 'name')
        self.status = self._try_except(data['metadata'], 'status')
        self.year = self._try_except(data['metadata'], 'seasonId')
        self.server_date = self._try_except(data['metadata'], 'serverDate')
        self._fetch_roster_settings(data)
        self._fetch_tie_rules(data)

    def __repr__(self):
        return 'Settings(%s)' % (self.name)

    def _try_except(self, data, key):
        '''Populate attributes'''
        try:
            return data[key]
        except:
            return "Unknown"

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
        self.tie_rule = self._try_except(tie_map, tie_id)

        playoff_tie_map = {
                           -1: 'Head to Head Record',
                           0: 'Total Points For',
                           1: 'Intra Division Record',
                           2: 'Total Points Against'
                          }

        playoff_id = data['leaguesettings']['playoffSeedingTieRuleRawStatId']
        self.playoff_seed_tie_rule = self._try_except(playoff_tie_map, playoff_id)
