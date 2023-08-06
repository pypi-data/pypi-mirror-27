import pytest

from crapipy import AsyncClient, Client


def assert_popular_clans(popular_clans):
    """Actual tests."""
    assert len(popular_clans) > 0

    for clan in popular_clans[:2]:
        assert int(clan.popularity.hits) > 0
        assert float(clan.popularity.hits_per_day_avg) > 0
        assert clan.tag is not None
        assert clan.name is not None

@pytest.mark.asyncio
async def test_popular_clans_async():
    """Test popular clans."""
    client = AsyncClient()
    popular_clans = await client.get_popular_clans()
    assert_popular_clans(popular_clans)


def test_popular_clans():
    """Text popular clans."""
    client = Client()
    popular_clans = client.get_popular_clans()
    assert_popular_clans(popular_clans)

