"""The Base Game code.
"""
from decimal import Decimal
from urllib.parse import urljoin

import requests

from .exceptions import (ConnectToServerException, NotSetupException,
                         ServerResponseException, WrongElvesException)

_BASE_SERVER_URL = 'https://elves.pythonnortheast.com'


class BaseGame:
    """The Base Game that we extend from.
    """

    MAX_TURNS = 10
    PLAYER_NAME = None
    SERVER_URL = _BASE_SERVER_URL

    def __init__(self):
        """Initialize the game.
        """
        if not self.PLAYER_NAME:
            raise NotSetupException(
                'You must set PLAYER_NAME on {}'.format(
                    self.__class__.__name__))

        uuid, elves, money = self.start_session()
        self._session_id = uuid
        self._elves_remaining = elves
        self._money_made = money

    def run(self):
        """Execute the game engine.
        """
        elves_available = self._elves_remaining
        for turn in range(1, self.MAX_TURNS + 1):
            print('Playing turn: {}'.format(turn))
            wood, forest, mountain = self.turn(elves_available)

            if not self._enough_elves(wood, forest, mountain, elves_available):
                raise WrongElvesException(wood,
                                          forest,
                                          mountain,
                                          elves_available)

            print('Sending your elves:\n'
                  'Woods: {wood}\n'
                  'Forest: {forest}\n'
                  'Mountains: {mountain}'.format(wood=wood,
                                                 forest=forest,
                                                 mountain=mountain))

            data = self._send_day(wood, forest, mountain)
            self._money_made = Decimal(data['money_made'])
            self._elves_remaining = elves_available = data['elves_remaining']
            self._weather = data['weather']

    def start_session(self):
        """Generate a Session ID and return it.
        """
        rtn = requests.post(self._generate_url('game/'),
                            {'player_name': self.PLAYER_NAME})
        return rtn['uuid'], rtn['elves_remaining'], Decimal(rtn['money_made'])

    def _generate_url(self, path):
        """Get the URL.
        """
        return urljoin(self.SERVER_URL, path)

    def _day_url(self):
        """Return the day_url.
        """
        path = 'game/{s._session_id}/day/'.format(s=self)
        return urljoin(self.SERVER_URL, path)

    def _send_day(self, wood, forest, mountain):
        """Send the day to the server.

        Assumes the elves have been calculated correctly.
        """
        response = requests.post(self._day_url(),
                                 json={'elves_woods': wood,
                                       'elves_forest': forest,
                                       'elves_mountains': mountain})

        if response.status_code != 201:
            if response.status_code == 400:
                raise ServerResponseException(response)
            else:
                raise ConnectToServerException(response)

        return response.json()

    def _enough_elves(self, woods, forest, mountain, total):
        """A quick client-side check to make sure we have enough elves to send.
        """
        return (woods + forest + mountain) == total
