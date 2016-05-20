ESPN Fantasy Football API
==============

A simple API for ESPN fantasy football.

Installation
------------

With Pip:

```bash
git clone https://github.com/rbarton65/espnff

python3 setup.py install
```

Usage
-----

This API returns information in JSON format on PUBLIC leagues. You can gather information on teams as well as calculate unbiased power rankings for any given week.

```python
import espnff

league_id = '''insert league id'''
year = '''insert league year'''

league = League(league_id, year)

team_id = '''insert team id'''

# grab season information on team
league.get_member(team_id)

# grab season information on all teams
league.get_all_members()

# grab power rankings for any week
league.get_week(week)
```
