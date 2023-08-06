import pytest

from crapipy import AsyncClient, Client


def assert_popular_tournaments(tournaments):
    """Actual tests."""
    assert len(tournaments) > 0

    for tournament in tournaments[:2]:
        assert int(tournament.popularity.hits) > 0
        assert float(tournament.popularity.hits_per_day_avg) > 0
        assert tournament.tag is not None
        assert tournament.name is not None

@pytest.mark.asyncio
async def test_popular_tournaments_async():
    """Test popular tournaments."""
    client = AsyncClient()
    popular_tournaments = await client.get_popular_tournaments()
    assert_popular_tournaments(popular_tournaments)


def test_popular_tournaments():
    """Text popular tournaments."""
    client = Client()
    popular_tournaments = client.get_popular_tournaments()
    assert_popular_tournaments(popular_tournaments)

