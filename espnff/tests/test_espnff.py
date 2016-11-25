import requests_mock
import unittest
import json


from espnff.espnff import (League,
                           PrivateLeagueException,
                           InvalidLeagueException,
                           UnknownLeagueException)


class LeagueTestCase(unittest.TestCase):
    '''Test League class'''

    @requests_mock.Mocker()
    def test_public_league(self, m):
        '''Is the status code 200 when calling a public league?'''
        data = json.loads(open('espnff/tests/test_league.json').read())
        m.get('http://games.espn.com/ffl/api/v2/leagueSettings?leagueId=1234&seasonId=2016', status_code=200, json=data)
        league = League(1234, 2016)
        self.assertEqual(league.status, 200)

    @requests_mock.Mocker()
    def test_private_league(self, m):
        '''Does the correct exception raise when the status code is 401?'''
        data = {"error": [{"message": "No permission to view this league", "code": "functional"}]}
        m.get('http://games.espn.com/ffl/api/v2/leagueSettings?leagueId=1234&seasonId=2016', status_code=401, json=data)
        with self.assertRaises(PrivateLeagueException):
            League(1234, 2016)

    @requests_mock.Mocker()
    def test_invalid_league(self, m):
        '''Does the correct exception raise when the status code is 404?'''
        data = {"error": [{"message": "Unable to retrieve league (2016:1234)", "code": "functional"}]}
        m.get('http://games.espn.com/ffl/api/v2/leagueSettings?leagueId=1234&seasonId=2016', status_code=404, json=data)
        with self.assertRaises(InvalidLeagueException):
            League(1234, 2016)

    @requests_mock.Mocker()
    def test_unknown_error(self, m):
        '''Does the correct exception raise when the status code is not 200, 401, or 404?'''
        data = {"error": [{"message": "java.lang.NullPointerException", "code": "exception"}]}
        m.get('http://games.espn.com/ffl/api/v2/leagueSettings?leagueId=1234&seasonId=2016', status_code=500, json=data)
        with self.assertRaises(UnknownLeagueException):
            League(1234, 2016)

    @requests_mock.Mocker()
    def test_team_length(self, m):
        '''Did all the teams load into the class?'''
        data = json.loads(open('espnff/tests/test_league.json').read())
        m.get('http://games.espn.com/ffl/api/v2/leagueSettings?leagueId=1234&seasonId=2016', status_code=200, json=data)
        league = League(1234, 2016)
        self.assertEqual(len(league.teams), 12)

    @requests_mock.Mocker()
    def test_team_scores(self, m):
        '''Do the sum of the scores attributes equal the points for?'''
        data = json.loads(open('espnff/tests/test_league.json').read())
        m.get('http://games.espn.com/ffl/api/v2/leagueSettings?leagueId=1234&seasonId=2016', status_code=200, json=data)
        league = League(1234, 2016)
        for team in league.teams:
            print(team.scores)
            self.assertAlmostEqual(sum(team.scores[:13]), team.points_for)

    @requests_mock.Mocker()
    def test_power_rankings(self, m):
        '''Does the power rankings algorithm have the expected output?'''
        data = json.loads(open('espnff/tests/test_league.json').read())
        m.get('http://games.espn.com/ffl/api/v2/leagueSettings?leagueId=1234&seasonId=2016', status_code=200, json=data)
        expected = ['22.45', '18.85', '17.80', '17.65', '17.00', '16.45',
                    '15.15', '14.80', '13.75', '13.00', '11.55', '8.45']
        league = League(1234, 2016)
        for points, num in zip(league.power_rankings(1), expected):
            self.assertEqual(points[0], num)

    @requests_mock.Mocker()
    def test_power_rankings_length(self, m):
        '''Does the power rankings algorithm output include all teams?'''
        data = json.loads(open('espnff/tests/test_league.json').read())
        m.get('http://games.espn.com/ffl/api/v2/leagueSettings?leagueId=1234&seasonId=2016', status_code=200, json=data)
        league = League(1234, 2016)
        for num in range(1, 13):
            self.assertEqual(len(league.power_rankings(num)), 12)
=======

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
>>>>>>> develop


if __name__ == '__main__':
    unittest.main()
