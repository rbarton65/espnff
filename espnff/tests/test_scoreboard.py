import requests_mock
import unittest
import json


from espnff.league import (League)
from espnff.exception import (PrivateLeagueException,
                              InvalidLeagueException,
                              UnknownLeagueException, )


class ScoreboardTestCase(unittest.TestCase):
    '''Test Scoreboard funtion'''

    def setUp(self):
        self.data = json.loads(open('espnff/tests/test_league.json').read())
        self.scoreboard_data = json.loads(open('espnff/tests/test_scoreboard.json').read())
        self.scoreboard_expected = ["Matchup(Team(Team 2), Team(Team 7))", "Matchup(Team(Team 1), Team(Team 11))",
                                    "Matchup(Team(Team 6), Team(Team 9))", "Matchup(Team(Team 12), Team(Team 4))",
                                    "Matchup(Team(Team 10), Team(Team 3))", "Matchup(Team(Team 8), Team(Team 5))"]

    @requests_mock.Mocker()
    def test_public_scoreboard(self, m):
        '''Is the status code 200 when calling a public league?'''
        m.get('http://games.espn.com/ffl/api/v2/leagueSettings?leagueId=1234&seasonId=2016',
              status_code=200, json=self.data)
        m.get('http://games.espn.com/ffl/api/v2/scoreboard?leagueId=1234&seasonId=2016',
              status_code=200, json=self.scoreboard_data)
        league = League(1234, 2016)
        league.scoreboard()
        self.assertEqual(league.status, 200)

    @requests_mock.Mocker()
    def test_private_scoreboard(self, m):
        '''Does the correct exception raise when the status code is 401?'''
        scoreboard_error = {"error": [{"message": "No permission to view this league", "code": "functional"}]}
        m.get('http://games.espn.com/ffl/api/v2/leagueSettings?leagueId=1234&seasonId=2016',
              status_code=200, json=self.data)
        m.get('http://games.espn.com/ffl/api/v2/scoreboard?leagueId=1234&seasonId=2016',
              status_code=401, json=scoreboard_error)
        with self.assertRaises(PrivateLeagueException):
            league = League(1234, 2016)
            league.scoreboard()

    @requests_mock.Mocker()
    def test_invalid_scoreboard(self, m):
        '''Does the correct exception raise when the status code is 404?'''
        scoreboard_error = {"error": [{"message": "Unable to retrieve league (2016:1234)", "code": "functional"}]}
        m.get('http://games.espn.com/ffl/api/v2/leagueSettings?leagueId=1234&seasonId=2016',
              status_code=200, json=self.data)
        m.get('http://games.espn.com/ffl/api/v2/scoreboard?leagueId=1234&seasonId=2016',
              status_code=404, json=scoreboard_error)
        with self.assertRaises(InvalidLeagueException):
            league = League(1234, 2016)
            league.scoreboard()

    @requests_mock.Mocker()
    def test_unknown_scoreboard(self, m):
        '''Does the correct exception raise when the status code is 500?'''
        scoreboard_error = {"error": [{"message": "java.lang.NullPointerException", "code": "functional"}]}
        m.get('http://games.espn.com/ffl/api/v2/leagueSettings?leagueId=1234&seasonId=2016',
              status_code=200, json=self.data)
        m.get('http://games.espn.com/ffl/api/v2/scoreboard?leagueId=1234&seasonId=2016',
              status_code=500, json=scoreboard_error)
        with self.assertRaises(UnknownLeagueException):
            league = League(1234, 2016)
            league.scoreboard()

    @requests_mock.Mocker()
    def test_scoreboard_week(self, m):
        '''Does the correct url generate from params when a week is entered?'''
        m.get('http://games.espn.com/ffl/api/v2/leagueSettings?leagueId=1234&seasonId=2016',
              status_code=200, json=self.data)
        m.get('http://games.espn.com/ffl/api/v2/scoreboard?leagueId=1234&seasonId=2016&matchupPeriodId=12',
              status_code=200, json=self.scoreboard_data)
        league = League(1234, 2016)
        league.scoreboard(week=12)
        self.assertEqual(league.status, 200)

    @requests_mock.Mocker()
    def test_scoreboard(self, m):
        '''Does the correct output return?'''
        m.get('http://games.espn.com/ffl/api/v2/leagueSettings?leagueId=1234&seasonId=2016',
              status_code=200, json=self.data)
        m.get('http://games.espn.com/ffl/api/v2/scoreboard?leagueId=1234&seasonId=2016',
              status_code=200, json=self.scoreboard_data)
        league = League(1234, 2016)
        scoreboard = league.scoreboard()
        scoreboard = [str(x) for x in scoreboard]
        self.assertEqual(scoreboard, self.scoreboard_expected)


if __name__ == '__main__':
    unittest.main()
