import pytest

from crapipy import AsyncClient, Client


def assert_top_players(top_players, location=''):
    assert len(top_players) > 0
    assert top_players[0].rank == 1
    if location != '':
        pass


@pytest.mark.asyncio
async def test_top_players_async():
    client = AsyncClient()
    top_players = await client.get_top_players()
    assert_top_players(top_players)


def test_top_players():
    client = Client()
    top_players = client.get_top_players()
    assert_top_players(top_players)

@pytest.mark.asyncio
async def test_top_local_players_async():
    """Test top clans."""
    client = AsyncClient()
    locatiion = 'us'
    top_players = await client.get_top_players(locatiion)
    assert_top_players(top_players, locatiion)


def test_top_local_players():
    """Text top clans."""
    client = Client()
    locatiion = 'us'
    top_players = client.get_top_players(locatiion)
    assert_top_players(top_players, locatiion)
