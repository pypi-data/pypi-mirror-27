import pytest

from crapipy import AsyncClient, Client


def assert_popular_players(popular_players):
    """Actual tests."""
    assert len(popular_players) > 0

    for player in popular_players[:2]:
        assert int(player.popularity.hits) > 0
        assert float(player.popularity.hits_per_day_avg) > 0
        assert player.tag is not None
        assert player.name is not None

@pytest.mark.asyncio
async def test_popular_players_async():
    """Test popular players."""
    client = AsyncClient()
    popular_players = await client.get_popular_players()
    assert_popular_players(popular_players)


def test_popular_players():
    """Text popular players."""
    client = Client()
    popular_players = client.get_popular_players()
    assert_popular_players(popular_players)

