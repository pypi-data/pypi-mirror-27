"""
cr-api client for Clash Royale.
"""
import json
import logging
import os

import requests
from requests.exceptions import HTTPError

from .exceptions import APIError
from .models import Clan, TopClans, Player, Constants, Tag, TopPlayers
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
            self._token = os.environ['TOKEN']
        return self._token

    def fetch(self, url):
        """Fetch URL.

        :param url: URL
        :return: Response in JSON

        """
        headers = {'auth': self.token}
        try:
            r = requests.get(url, headers=headers)
            data = r.json()

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

    def get_top_clans(self):
        """Fetch top clans."""
        data = self.fetch(APIURL.top_clans)
        return TopClans(data)

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

    def get_constants(self, key=None):
        """Fetch contants.

        :param key: Optional field.
        """
        url = APIURL.constants
        data = self.fetch(url)
        return Constants(data)

    def get_top_players(self):
        """Fetch top players."""
        url = APIURL.top_players
        data = self.fetch(url)
        return TopPlayers(data)
