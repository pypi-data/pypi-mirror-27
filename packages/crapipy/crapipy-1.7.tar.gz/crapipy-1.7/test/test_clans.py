import pytest

from crapipy import AsyncClient, Client


def assert_clans(clans):
    """Run tests."""
    assert clans[0].name == 'Reddit Alpha'
    assert clans[0].badge.name == 'A_Char_Rocket_02'
    assert clans[1].name == 'Reddit Bravo'
    assert clans[1].badge.name == 'A_Char_Rocket_02'


@pytest.mark.asyncio
async def test_clans_async():
    client = AsyncClient()
    clans = await client.get_clans(['2CCCP', '2U2GGQJ'])
    assert_clans(clans)


def test_clans():
    client = Client()
    clans = client.get_clans(['2CCCP', '2U2GGQJ'])
    assert_clans(clans)


