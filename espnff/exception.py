class ESPNFFException(Exception):
    pass


class PrivateLeagueException(ESPNFFException):
    pass


class InvalidLeagueException(ESPNFFException):
    pass


class UnknownLeagueException(ESPNFFException):
    pass
