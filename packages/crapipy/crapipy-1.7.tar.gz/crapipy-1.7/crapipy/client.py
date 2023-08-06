"""
cr-api client for Clash Royale.
"""
import json
import logging
import os

import requests
from requests.exceptions import HTTPError

from .exceptions import APIError
from .models import Clan, Clans, Player, Constants, Tag, Players, Tournament, EndPoints, Tournaments
from .url import APIURL

logger = logging.getLogger('__name__')
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.ERROR)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)


class Client:
    """
    API Client.
    """

    def __init__(self, token=None):
        self._token = token

    @property
    def token(self):
        """Load token from environment if not defined"""
        if self._token is None:
            self._token = os.environ.get('TOKEN')
        return self._token

    def fetch(self, url, is_json=True):
        """Fetch URL.

        :param url: URL
        :return: Response in JSON

        """
        headers = {'auth': self.token}
        try:
            r = requests.get(url, headers=headers)
            if is_json:
                data = r.json()
            else:
                data = r.text

            if r.status_code != 200:
                logger.error(
                    "API Error | HTTP status {status} | url: {url}".format(
                        status=r.status_code,
                        url=url
                    )
                )
                raise APIError(**data)

            if isinstance(data, dict):
                if data.get('error'):
                    raise APIError(**data)

        except (HTTPError, ConnectionError, json.JSONDecodeError):
            raise APIError

        return data

    def get_clan(self, clan_tag):
        """Fetch a single clan."""
        url = APIURL.clan.format(clan_tag)
        data = self.fetch(url)
        return Clan(data)

    def get_clans(self, clan_tags):
        """Fetch multiple clans.

        :param clan_tags: List of clan tags
        """
        url = APIURL.clan.format(','.join(clan_tags))
        data = self.fetch(url)
        return [Clan(d) for d in data]

    def get_player(self, tag: str):
        """Get player profile by tag.
        :param tag:
        :return:
        """
        ptag = Tag(tag).tag
        url = APIURL.player.format(ptag)
        data = self.fetch(url)
        return Player(data)

    def get_players(self, tags):
        """Fetch multiple players from profile API."""
        ptags = [Tag(tag).tag for tag in tags]
        url = APIURL.player.format(','.join(ptags))
        data = self.fetch(url)
        return [Player(d) for d in data]

    def get_tournament(self, tag):
        """Get tournament detail."""
        url = APIURL.tournaments.format(tag)
        data = self.fetch(url)
        return Tournament(data)

    def get_constants(self, key=None):
        """Fetch contants.

        :param key: Optional field.
        """
        url = APIURL.constants
        data = self.fetch(url)
        return Constants(data)

    def get_top_players(self, location=''):
        """Fetch top players."""
        url = APIURL.top_players.format(location)
        data = self.fetch(url)
        return Players(data)

    def get_top_clans(self, location=''):
        """Fetch top clans."""
        url = APIURL.top_clans.format(location)
        data = self.fetch(url)
        return Clans(data)

    def get_endpoints(self):
        """Endpoints"""
        url = APIURL.endpoints
        data = self.fetch(url)
        return EndPoints(data)

    def get_version(self):
        """API verision."""
        url = APIURL.version
        data = self.fetch(url, is_json=False)
        return data

    def get_popular_players(self):
        """Fetch popular players."""
        url = APIURL.popular_players
        data = self.fetch(url)
        return Players(data)

    def get_popular_clans(self):
        """Fetch popular clans."""
        url = APIURL.popular_clans
        data = self.fetch(url)
        return Clans(data)

    def get_popular_tournaments(self):
        """Fetch popular tournaments."""
        url = APIURL.popular_tournaments
        data = self.fetch(url)
        return Tournaments(data)
