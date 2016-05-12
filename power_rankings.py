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
            yield Members(team_name, team_id, self.league_id, self.year)


class Members(object):
    wins = [0]*32
    mov = []
    opponents = []
    scores = []
    previous_rank = 0
    current_rank = 0
    power_points = 0

    def __init__(self, name, team_id, league_id, year):
        self.name = name
        self.team_id = team_id
        self.league_id = league_id
        self.year = year

    def get_info(self):
        url = "http://games.espn.go.com/ffl/schedule?leagueId=%s&teamId=%s&seasonId=%s"
        page = requests.get(url % (self.league_id, self.team_id, self.year))
        tree = html.fromstring(page.content)
        self.scores = [x.text[2:].split('-')[0] for x in tree.xpath('//table//tr[@bgcolor]//td//nobr//a')][:13]
        self.opponents = [re.compile('teamId=(.*?)&').search(x.attrib['href']).group(1) for x in tree.xpath('//table//tr[@bgcolor]//td[@nobr=""]//a')][:13]
        self.mov = ["{0:.2f}".format(float(x.text[2:].split('-')[0]) - float(x.text.split('-')[1])) for x in tree.xpath('//table//tr[@bgcolor]//td//nobr//a') if "pts" not in x.text][:13]

def main():
    league = League(288077, 2015)
    members = league.gather_members()
#    [x.get_info() for x in members]
	
if  __name__ =='__main__':main()
	
