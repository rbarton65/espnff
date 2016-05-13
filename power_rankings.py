import re
# import argparse
from lxml import html

import requests

'''
parser = argparse.ArgumentParser()
parser.add_argument('-l', '--league',
                    help='ESPN league ID',
                    required=True)
parser.add_argument('-w','--week',
                    help='power ranking for this week',
                    required=True)
parser.add_argument('-y','--year',
                    help='power ranking for this year',
                    required=True)
args = parser.parse_args()
'''


class League(object):

    def __init__(self, league_id, year):
        self.league_id = league_id
        self.year = year

    def fetch_members(self):
        '''Fetch members in league'''
        url = 'http://games.espn.go.com/ffl/standings?leagueId=%s&seasonId=%s'
        page = requests.get(url % (self.league_id, self.year))
        tree = html.fromstring(page.content)

        for member in tree.xpath('//tr[@class="tableBody"]//td//a'):
            team_name = member.text
            # parse team id from href url
            keysearch = re.compile('teamId=(.*?)&')
            team_id = keysearch.search(member.attrib['href']).group(1)
            yield(Members(team_name, team_id, self.league_id, self.year))


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
        self.wins = [0]*32  # team_id numbers increase with new members, 32 to be safe
        self.fetch_info()
        self.calculate_wins()

    def fetch_info(self):
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

    def calculate_wins(self):
        '''Calculates wins based on negative or positive margin of victory'''
        # create tuple to determine outcome against opponents
        outcomes = list(zip(self.opponents, self.mov))
        # convert to ints and floats
        outcomes = [(int(x), float(y)) for (x, y) in outcomes]

        for opp, mov in outcomes:
            opp = opp-1  # team id 1 is 0th place in self.wins
            if mov > 0:
                self.wins[opp] += 1


def main():
    league = League(288077, 2015)
    # create list from generator
    members = list(league.fetch_members())
    # create matrix of every members' wins
    matrix = [x.wins for x in members]
    print(matrix)


if __name__ == '__main__':
    main()
