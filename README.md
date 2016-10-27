[![Build Status](https://travis-ci.org/rbarton65/espnff.svg?branch=master)](https://travis-ci.org/rbarton65/espnff) [![version](https://img.shields.io/badge/version-1.1.0-blue.svg)](https://github.com/rbarton65/espnff/blob/master/CHANGELOG.md) [![PyPI version](https://badge.fury.io/py/espnff.svg)](https://badge.fury.io/py/espnff)

# ESPN Fantasy Football API

Using ESPN's Fantasy Football private API, this package interfaces with 
ESPN Fantasy Football to gather data from any public league. A good way to mine data
without webscraping for data manipulation projects.

## Getting Started

These instructions will get you a copy of the project up and running 
on your local machine for development and testing purposes.

### Installing
With pip:

```python3
pip3 install espnff
```

With Git:

```bash
git clone https://github.com/rbarton65/espnff

cd espnff

python3 setup.py install
```


## Basic Usage

This gives an overview of all the features of `espnff`

### Downloading a public league

```python3
>>> from espnff import League
>>> league_id = 123456
>>> year = 2016
>>> league = League(league_id, year)
>>> league
League 123456, 2016 Season
```

### Viewing teams in a public league

```python3
>>> from espnff import League
>>> league_id = 123456
>>> year = 2016
>>> league = League(league_id, year)
>>> league.teams
[Team 1, Team 2, Team 3, Team 4, Team 5, Team 6, Team 7, Team 8]
>>> team1 = league.teams[0]
>>> team1
Team 1
```

### Viewing data for specific team

```python3
>>> league.teams
[Team 1, Team 2, Team 3, Team 4, Team 5, Team 6, Team 7, Team 8]
>>> team1 = league.teams[0]
>>> team1.team_id
1
>>> team1.team_name
Team 1
>>> team1.team_abbrev
T1
>>> team1.owner
Roger Goodell
>>> team1.division_id
0
>>> team1.division_name
Division 1
>>> team1.wins
5
>>> team1.losses
1
>>> team1.points_for
734.69
>>> team1.points_against
561.15
>>> team1.schedule
[Team 2, Team 3, Team 4, Team 5, Team 6, Team 7, Team 8, Team 2, Team 3, Team 4, Team 5, Team 6, Team 7, Team 8]
>>> team1.scores
[135.5, 126.38, 129.53, 126.65, 114.81, 101.82, 1.15, 0, 0, 0, 0, 0, 0, 0]
>>> team1.mov
[32.12, 24.92, 45.97, 34.17, 41.74, -5.39, 1.15, 0, 0, 0, 0, 0, 0, 0]
```

### Viewing power rankings

```python3
>>> from espnff import League
>>> league_id = 123456
>>> year = 2016
>>> league = League(league_id, year)
>>> league.power_rankings(week=5)
[('31.85', Team 1), ('25.60', Team 3), ('25.60', Team 6), ('22.45', Team 2), 
('20.70', Team 8), ('18.20', Team 7), ('18.20', Team 4), ('18.10', Team 5)]
```

## Running the tests

Automated tests for this package are included in the `tests` directory. After installation,
you can run these tests by changing the directory to the `espnff` directory and running the following:

```python3
python3 setup.py test
```

## Versioning

This library uses [SemVer](http://semver.org/) for versioning. For available versions, see the
[tags on this repository](https://github.com/rbarton65/espnff/tags)
