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
		
class Members(League):
	wins = [0]*32
	mov = []
	opponents = []
	scores = []
	previous = 0
	current = 0
	rank = 0
	def __init__(self, name, team_id, league_id, year):
		self.name = name 
		self.team_id = team_id
		super(Members, self).__init__(league_id, year)
	def get_info(self):
		page = requests.get("http://games.espn.go.com/ffl/schedule?leagueId=%s&teamId=%s&seasonId=%s" % (self.league_id, self.team_id, self.year))
		tree = html.fromstring(page.content)
		self.scores = [x.text[2:].split('-')[0] for x in tree.xpath('//table//tr[@bgcolor]//td//nobr//a')]
#		self.opponents = ([re.compile('teamId=(.*?)&').search(x.attrib['href']).group(1) for x in tree.xpath('//table//tr[@bgcolor]//td[@nobr=""]//a')[:13])
#		print(tree.xpath('//table//tr[@bgcolor]//td[@nobr=""]//a')[:13])
#		self.mov = (["{0:.2f}".format(float(x.text[2:].split('-')[0]) - float(x.text.split('-')[1])) for x in tree.xpath('//table//tr[@bgcolor]//td//nobr//a')])

def main():
	league = League(288077, 2015)
	league.gather_members()
	members = [Members(i,j, 288077, 2015) for (i,j) in league.members.items()]
	[x.get_info() for x in members]
	print ([x.opponents for x in members])
	
if  __name__ =='__main__':main()
	
