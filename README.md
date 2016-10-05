ESPN Fantasy Football API
==============

A simple API for ESPN fantasy football.

Installation
------------
With pip:
```python
pip3 install espnff
```


With Git:

```bash
git clone https://github.com/rbarton65/espnff

python3 setup.py install
```

Usage
-----

This package interfaces with ESPN Fantasy Football to gather data from any public league.

League class
-----

The League class has is created with a league ID and league year. League can return the members of any league instance.

```python
from espnff import League

league_id = '''insert league id'''
year = '''insert league year'''

league = League(league_id, year)

print(league.members)
```

Member class
-----

The Member class has the following attributes for each member of the league:

```
teamId # ID of team
teamAbbrev # abbreviation of team
teamName # name of team
divisionID # ID of division
divisionName # name of division
wins # number of wins
losses # number of losses
pointsFor # total points scored by team
pointsAgainst # total points scored against team
owner # owner of team's name
schedule # list of opponents for team
scores # score of each week
```
```
