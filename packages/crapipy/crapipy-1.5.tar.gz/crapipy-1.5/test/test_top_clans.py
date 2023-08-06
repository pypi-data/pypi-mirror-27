import pytest

from crapipy import AsyncClient, Client


def assert_top_clans(top_clans, location=''):
    """Actual tests."""
    assert len(top_clans) > 0
    if location != '':
        assert top_clans[0].location.code == location.upper()


@pytest.mark.asyncio
async def test_top_clans_async():
    """Test top clans."""
    client = AsyncClient()
    top_clans = await client.get_top_clans()
    assert_top_clans(top_clans)


def test_top_clans():
    """Text top clans."""
    client = Client()
    top_clans = client.get_top_clans()
    assert_top_clans(top_clans)


@pytest.mark.asyncio
async def test_top_local_clans_async():
    """Test top clans."""
    client = AsyncClient()
    locatiion = 'us'
    top_clans = await client.get_top_clans(locatiion)
    assert_top_clans(top_clans, locatiion)


def test_top_local_clans():
    """Text top clans."""
    client = Client()
    locatiion = 'us'
    top_clans = client.get_top_clans(locatiion)
    assert_top_clans(top_clans, locatiion)
