import re
# import argparse
from lxml import html

import requests

'''
parser = argparse.ArgumentParser()
parser.add_argument("-l", "--league", help="ESPN league ID", required=True)
parser.add_argument("-w","--week",
                    help="power ranking for this week",
                    required=True)
parser.add_argument("-y","--year",
                    help="power ranking for this year",
                    required=True)
args = parser.parse_args()
'''


class League(object):

    def __init__(self, league_id, year):
        self.league_id = league_id
        self.year = year

    def gather_members(self):
        url = "http://games.espn.go.com/ffl/standings?leagueId=%s&seasonId=%s"
        page = requests.get(url % (self.league_id, self.year))
        tree = html.fromstring(page.content)
        for member in tree.xpath('//tr[@class="tableBody"]//td//a'):
            team_name = member.text
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
        self.wins = [0]*32

    def get_info(self):
        url = "http://games.espn.go.com/ffl/schedule?leagueId=%s&teamId=%s&seasonId=%s"
        page = requests.get(url % (self.league_id, self.team_id, self.year))
        tree = html.fromstring(page.content)
        for score in tree.xpath('//table//tr[@bgcolor]//td//nobr//a')[:13]:
            self.scores.append((score.text[2:].split('-')[0]))
        for opp in tree.xpath('//table//tr[@bgcolor]//td[@nobr=""]//a')[:13]:
            keysearch = re.compile('teamId=(.*?)&')
            self.opponents.append(keysearch.search(opp.attrib['href']).group(1))
        for score in tree.xpath('//table//tr[@bgcolor]//td//nobr//a')[:13]:
            if "pts" not in score.text:
                team_score = float(score.text[2:].split('-')[0])
                opp_score = float(score.text.split('-')[1])
                self.mov.append("{0:.2f}".format(team_score - opp_score))


def main():
    league = League(288077, 2015)
    members = [member for member in league.gather_members()]
    print([x.mov for x in members])
    [x.get_info() for x in members]
    for x in members:
        print(x.mov)

if __name__ == '__main__': main()
