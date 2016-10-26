import requests_mock
import unittest
import json


from espnff.espnff import League


class LeagueTestCase(unittest.TestCase):
    '''Test League class'''

    @requests_mock.Mocker()
    def test_public_league(self, m):
        '''Is the status code 200 when calling a public league?'''
        data = json.loads(open('espnff/tests/test_league.json').read())
        m.get('http://games.espn.com/ffl/api/v2/leagueSettings?leagueId=1234&seasonId=2016', status_code=200, json=data)
        league = League(1234, 2016)
        self.assertEqual(league.status, 200)

if __name__ == '__main__':
    unittest.main()
