import argparse
from lxml import html
import requests
import re
'''
parser = argparse.ArgumentParser()
parser.add_argument("-l", "--league", help="ESPN league ID", required=True)
parser.add_argument("-w","--week", help="power ranking for this week", required=True)
parser.add_argument("-y","--year", help="power ranking for this year", required=True)
args = parser.parse_args()
'''
class League(object):
	members = {}
	def __init__(self, league_id, year):
		self.league_id = league_id
		self.year = year
	
	def gather_members(self):
		page = requests.get("http://games.espn.go.com/ffl/standings?leagueId=%s&seasonId=%s" % (self.league_id, self.year))
		tree = html.fromstring(page.content)
		self.members = {x.text : re.compile('teamId=(.*?)&').search(x.attrib['href']).group(1) for x in tree.xpath('//tr[@class="tableBody"]//td//a')}
		
class Members(object):
	wins = [0]*32
	mov = []
	scores = []
	previous = 0
	current = 0
	rank = 0
	def __init__(self, name, team_id):
		self.name = name 
		self.team_id = team_id

def main():
	league = League(288077, 2015)
	league.gather_members()
	members = [Members(i,j) for (i,j) in league.members.items()]

if  __name__ =='__main__':main()
	
