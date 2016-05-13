import re

from lxml import html

import requests

import utils


class League(object):

    def __init__(self, league_id, year):
        self.league_id = league_id
        self.year = year
        self.members = []
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

    def get_week(self, week):
        '''Get power rankings for specified week'''
        wins_matrix = [x.calculate_wins(week) for x in self.members]
        # calculate two step dominance
        dominance_list = utils.two_step_dominance(wins_matrix)
        # assign dominance number to each team
        for dom, team in zip(dominance_list, self.members):
            team.dominance = dom


class Members(object):

    def __init__(self, name, team_id, league_id, year):
        self.name = name
        self.team_id = team_id
        self.league_id = league_id
        self.year = year
        self.current_rank = 0
        self.mov = []
        self.opponents = []
        self.previous_rank = 0
        self.power_points = 0
        self.scores = []
        self.dominance = 0
        self._fetch_info()

    def _fetch_info(self):
        '''Fetch the scores, opponents, and margin of victory for each week'''
        url = 'http://games.espn.go.com/ffl/schedule?leagueId=%s&teamId=%s&seasonId=%s'
        page = requests.get(url % (self.league_id, self.team_id, self.year))
        tree = html.fromstring(page.content)

        # Fetch scores for regular season (13 weeks)
        for score in tree.xpath('//table//tr[@bgcolor]//td//nobr//a')[:13]:
            self.scores.append((score.text[2:].split('-')[0]))  # 'W 98-85' will return '98'

        # Fetch opponents for regular season
        for opp in tree.xpath('//table//tr[@bgcolor]//td[@nobr=""]//a')[:13]:
            keysearch = re.compile('teamId=(.*?)&')
            self.opponents.append(keysearch.search(opp.attrib['href']).group(1))

        # Fetch margin of victory for regular season
        for score in tree.xpath('//table//tr[@bgcolor]//td//nobr//a')[:13]:
            if 'pts' not in score.text:  # 'pts' appear on bye weeks
                team_score = float(score.text[2:].split('-')[0])  # 'W 98-85' will return '98', need float for decimals
                opp_score = float(score.text.split('-')[1])  # 'W 98-89' will return '85', need float for decimals
                self.mov.append('{0:.2f}'.format(team_score - opp_score))

    def _power_points(self):
        pass

    def calculate_wins(self, week):
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
        return wins


def main():
    league = League(288077, 2015)
    league.get_week(3)
    for x in league.members:
        print(x.name, x.dominance)


if __name__ == '__main__':
    main()
