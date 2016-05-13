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
            keysearch = re.compile('teamId=(.*?)&')
            team_id = keysearch.search(member.attrib['href']).group(1)  # parse team id from href url
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
        self.wins = [0]*32
        self.fetch_info()

    def fetch_info(self):
        '''Fetch the scores, opponents, and margin of victory for each week'''
        url = 'http://games.espn.go.com/ffl/schedule?leagueId=%s&teamId=%s&seasonId=%s'
        page = requests.get(url % (self.league_id, self.team_id, self.year))
        tree = html.fromstring(page.content)

        for score in tree.xpath('//table//tr[@bgcolor]//td//nobr//a')[:13]:  # regular season only (13 weeks)
            self.scores.append((score.text[2:].split('-')[0]))  # 'W 98-85' will return '98'

        for opp in tree.xpath('//table//tr[@bgcolor]//td[@nobr=""]//a')[:13]:  # regular season only (13 weeks)
            keysearch = re.compile('teamId=(.*?)&')
            self.opponents.append(keysearch.search(opp.attrib['href']).group(1))

        for score in tree.xpath('//table//tr[@bgcolor]//td//nobr//a')[:13]:  # regular season only (13 weeks)
            if 'pts' not in score.text:  # 'pts' appear on bye weeks
                team_score = float(score.text[2:].split('-')[0])  # 'W 98-85' will return '98', need float for decimals
                opp_score = float(score.text.split('-')[1])  # 'W 98-89' will return '85', need float for decimals
                self.mov.append('{0:.2f}'.format(team_score - opp_score))


def main():
    league = League(288077, 2015)
    members = list(league.fetch_members())  # create list from generator


if __name__ == '__main__':
    main()
