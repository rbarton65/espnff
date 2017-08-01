import requests_mock
import unittest
import json


from espnff.league import (League)
from espnff.exception import (PrivateLeagueException,
                              InvalidLeagueException,
                              UnknownLeagueException, )


class LeagueTestCase(unittest.TestCase):
    '''Test League class'''

    @requests_mock.Mocker()
    def test_public_league(self, m):
        '''Is the status code 200 when calling a public league?'''
        data = json.loads(open('tests/test_league.json').read())
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


if __name__ == '__main__':
    unittest.main()
