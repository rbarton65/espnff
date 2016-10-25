import requests
import unittest
import json
from unittest import mock


from espnff.espnff import League, Team


def mocked_requests_get(*args, **kwargs):
    class MockResponse:
        def __init__(self, data, status_code):
            self.data = data
            self.status_code = status_code

        def json(self):
            return self.data

    public_test = "http://games.espn.com/ffl/api/v2/leagueSettings?leagueId=1234&seasonId=2016"
    private_test = "http://games.espn.com/ffl/api/v2/leagueSettings?leagueId=4321&seasonId=2016"
    public_json = json.loads(open('test_league.json').read())
    private_error = {"error":[{"message":"No permission to view this league","code":"functional"}]}
    invalid_error = {"error":[{"message":"Unable to retrieve league (2016:9000000)","code":"functional"}]}
    params = kwargs['params']

    if "%s?leagueId=%s&seasonId=%s" % (args[0], params['leagueId'], params['seasonId']) == public_test:
        return MockResponse(public_json, 200)

    elif "%s?leagueId=%s&seasonId=%s" % (args[0], params['leagueId'], params['seasonId']) == private_test:
        return MockResponse(private_error, 401)

    else:
        return MockResponse(invalid_error, 404)


class LeagueTestCase(unittest.TestCase):

    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_public_league(self, mock_get):
        league = League(1234, 2016)
        self.assertEqual(league.json, {'league': 'public'})
        self.assertEqual(league.status, 200)

    @mock.patch('requests.get', side_effect=mocked_requests_get)   
    def test_private_league(self, mock_get):
        league = League(4321, 2016)
 #       self.assertEqual(league.json, {'league': 'private'})
        self.assertEqual(league.status, 401)

    @mock.patch('requests.get', side_effect=mocked_requests_get)   
    def test_invalid_league(self, mock_get):
        league = League(9000000, 2016)
#        self.assertEqual(league.json, {'league': 'invalid'})
        self.assertEqual(league.status, 404)

if __name__ == '__main__':
    unittest.main()
