import pytest

from crapipy import AsyncClient, Client


@pytest.mark.asyncio
async def test_top_players_async():
    client = AsyncClient()
    top_players = await client.get_top_players()
    assert len(top_players) > 0
    assert top_players[0].rank == 1


def test_top_players():
    client = Client()
    top_players = client.get_top_players()
    assert len(top_players) > 0
    assert top_players[0].rank == 1
