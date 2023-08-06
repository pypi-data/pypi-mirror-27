"""
cr-api async client for Clash Royale.
"""
import asyncio
import json
import logging
import os

import aiohttp

from .exceptions import APIError
from .models import Clan, Tag, Player, Constants, TopPlayers, TopClans
from .url import APIURL
from .util import make_box

logger = logging.getLogger('__name__')
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.ERROR)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)


class AsyncClient:
    """
    API AsyncClient.
    """

    def __init__(self, token=None):
        self._token = token

    @property
    def token(self):
        """Load token from environment if not defined"""
        if self._token is None:
            self._token = os.environ['TOKEN']
        return self._token

    async def fetch(self, url):
        """Fetch URL.

        :param url: URL
        :return: Response in JSON
        """
        headers = {'auth': self.token}
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers) as resp:
                    data = await resp.json()
                    if resp.status != 200:
                        logger.error(
                            "API Error | HTTP status {status} | {errmsg} | url: {url}".format(
                                status=resp.status,
                                errmsg=data.get('error'),
                                url=url
                            )
                        )
                        raise APIError(**data)

        except (asyncio.TimeoutError, aiohttp.ClientResponseError, json.JSONDecodeError):
            raise APIError

        return data

    async def get_clan(self, clan_tag):
        """Fetch a single clan."""
        url = APIURL.clan.format(clan_tag)
        data = await self.fetch(url)
        if isinstance(data, list):
            data = data[0]
        return Clan(data)

    async def get_clans(self, clan_tags):
        """Fetch multiple clans.

        :param clan_tags: List of clan tags
        """
        url = APIURL.clan.format(','.join(clan_tags))
        data = await self.fetch(url)
        return [Clan(d) for d in data]

    async def get_player(self, tag: str) -> Player:
        """Get player profile by tag.
        :param tag: 
        :return: 
        """
        ptag = Tag(tag).tag
        url = APIURL.player.format(ptag)
        data = await self.fetch(url)
        return Player(data)

    async def get_players(self, tags):
        """Fetch multiple players from profile API."""
        ptags = [Tag(tag).tag for tag in tags]
        url = APIURL.player.format(','.join(ptags))
        data = await self.fetch(url)
        return [Player(d) for d in data]

    async def get_constants(self, key=None):
        """Fetch contants.

        :param key: Optional field.
        """
        url = APIURL.constants
        data = await self.fetch(url)
        return Constants(data)

    async def get_top_players(self, location=''):
        """Fetch top players."""
        url = APIURL.top_players.format(location)
        data = await self.fetch(url)
        return TopPlayers(data)

    async def get_top_clans(self, location=''):
        """Fetch top clans."""
        url = APIURL.top_clans.format(location)
        data = await self.fetch(url)
        return TopClans(data)
