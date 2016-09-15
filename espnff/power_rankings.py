import re
import operator

import json
from lxml import html

import requests

from .utils import two_step_dominance


class League(object):

    def __init__(self, league_id, year):
        self.league_id = league_id
        self.year = year
        self.members = []
        self.basic_settings = {
                               'League Name': None,
                               'Number of Teams': None,
                               'Scoring Type': None
                               }
        self._fetch_members()

    def _fetch_members(self):
        '''Fetch members in league'''
        url = 'http://games.espn.go.com/ffl/standings?leagueId=%s&seasonId=%s'
        page = requests.get(url % (self.league_id, self.year))
        tree = html.fromstring(page.content)

        for member in tree.xpath('//tr[@class="tableBody"]//td//a'):
            team_name = member.text
            # parse team id from href url
            keysearch = re.compile('teamId=(.*?)&')
            team_id = keysearch.search(member.attrib['href']).group(1)
            self.members.append(Members(team_name, team_id, self.league_id, self.year))

    def _fetch_settings(self):
        '''Fetch settings for league'''
        url = 'http://games.espn.go.com/ffl/leaguesetup/settings?leagueId=%s&seasonId=%s'
        page = requests.get(url % (self.league_id, self.year))
        tree = html.fromstring(page.content)

    def _previous_ranking(self, week):
        '''Get last week power rankings for specified week'''
        week = week - 1
        wins_matrix = [x._calculate_wins(week) for x in self.members]
        # calculate two step dominance
        dominance_list = two_step_dominance(wins_matrix)

        # assign dominance number to each team, calculate power points
        for dom, team in zip(dominance_list, self.members):
            team.dominance = dom
            team._power_points(week)

        # sort by power points
        self.members.sort(key=operator.attrgetter('power_points'), reverse=True)

        for rank, team in enumerate(self.members):
            team.previous_rank = rank+1

    def _current_ranking(self, week):
        '''Get curent power rankings for specified week'''
        wins_matrix = [x._calculate_wins(week) for x in self.members]
        # calculate two step dominance
        dominance_list = two_step_dominance(wins_matrix)

        # assign dominance number to each team, calculate power points
        for dom, team in zip(dominance_list, self.members):
            team.dominance = dom
            team._power_points(week)

        # sort by power points
        self.members.sort(key=operator.attrgetter('power_points'), reverse=True)

        for rank, team in enumerate(self.members):
            team.current_rank = rank+1

    def get_week(self, week):
        '''Get power rankings for specified week'''
        if week > 1:
            self._previous_ranking(week)
            self._current_ranking(week)
        else:
            self._current_ranking(week)

        # build json object
        data = {int(x.current_rank): {
                        'name': x.name,
                        'losses': x.losses,
                        'power points': x.power_points,
                        'previous rank': x.previous_rank,
                        'wins': x.wins
                        }
                for x in self.members
                }
        json_data = json.dumps(data, sort_keys=True,
                               indent=4, separators=(',', ': '))
        return json_data

    def get_member(self, id):
        '''Get team information'''
        # find team with matching team id
        data = {int(x.team_id): {
                            'name': x.name,
                            'year': x.year,
                            'scores': x.scores,
                            'opponents': x.opponents,
                            'wins': x.wins,
                            'mov': x.mov
                            }
                for x in self.members if x.team_id == str(id)
                }
        json_data = json.dumps(data, sort_keys=True,
                               indent=4, separators=(',', ': '))
        return json_data

    def get_all_members(self):
        '''Get all member information'''
        data = {int(x.team_id): {
                            'name': x.name,
                            'year': x.year,
                            'scores': x.scores,
                            'opponents': x.opponents,
                            'wins': x.wins,
                            'mov': x.mov
                            }
                for x in self.members
                }
        json_data = json.dumps(data, sort_keys=True,
                               indent=4, separators=(',', ': '))
        return json_data


class Members(object):

    def __init__(self, name, team_id, league_id, year):
        self.name = name
        self.team_id = team_id
        self.league_id = league_id
        self.year = year
        self.current_rank = 0
        self.losses = 0
        self.mov = []
        self.opponents = []
        self.previous_rank = 0
        self.power_points = 0
        self.scores = []
        self.wins = 0
        self.dominance = 0
        self._fetch_info()

    def _fetch_info(self):
        '''Fetch the scores, opponents, and margin of victory for each week'''
        url = 'http://games.espn.go.com/ffl/schedule?leagueId=%s&teamId=%s&seasonId=%s'
        page = requests.get(url % (self.league_id, self.team_id, self.year))
        tree = html.fromstring(page.content)

        # Fetch scores for regular season (13 weeks)
        for score in tree.xpath('//table//tr[@bgcolor]//td//nobr//a')[:13]:
            try:
                self.scores.append(float(score.text[2:].split('-')[0]))  # 'W 98-85' will return '98'
            except:
                self.scores.append(float(0))

        # Fetch opponents for regular season
        for opp in tree.xpath('//table//tr[@bgcolor]//td[@nobr=""]//a')[:13]:
            keysearch = re.compile('teamId=(.*?)&')
            self.opponents.append(keysearch.search(opp.attrib['href']).group(1))

        # Fetch margin of victory for regular season
        for score in tree.xpath('//table//tr[@bgcolor]//td//nobr//a')[:13]:
            if 'pts' not in score.text:  # 'pts' appear on bye weeks
                try:
                    team_score = float(score.text[2:].split('-')[0])  # 'W 98-85' will return '98', need float for decimals
                    opp_score = float(score.text.split('-')[1])  # 'W 98-89' will return '85', need float for decimals
                except:
                    # Game hasn't happened yet
                    team_score = opp_score = 0
                mov = team_score - opp_score
                self.mov.append('{0:.2f}'.format(mov))
                if mov > 0:
                    self.wins += 1

    def _power_points(self, week):
        '''Calculate power points'''
        # turn needed values into floats
        self.scores = [float(x) for x in self.scores]
        self.mov = [float(x) for x in self.mov]
        self.dominance = float(self.dominance)
        score_avg = float('{0:.2f}'.format(sum(self.scores[:week]) / week))
        mov_avg = float('{0:.2f}'.format(sum(self.mov[:week]) / week))
        # formula is weighted 80% dominance, 15% scores, 5% margin of victory
        self.power_points = float('{0:.2f}'.format((self.dominance*0.8) +
                                                   (score_avg*0.15) +
                                                   (mov_avg*0.5)))

    def _calculate_wins(self, week):
        '''Calculates wins based on negative or positive margin of victory'''
        wins = [0]*32  # team_id numbers increase with new members, 32 to be safe
        # create tuple to determine outcome against opponents
        outcomes = list(zip(self.opponents, self.mov))
        # convert to ints and floats
        outcomes = [(int(x), float(y)) for (x, y) in outcomes]

        for opp, mov in outcomes[:week]:
            opp = opp-1  # team id 1 is 0th place in self.wins
            if mov > 0:
                wins[opp] += 1

        # set losses and wins
        self.losses = week - sum(wins)
        self.wins = sum(wins)

        return wins
