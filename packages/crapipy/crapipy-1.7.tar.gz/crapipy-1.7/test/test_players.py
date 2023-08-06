import pytest

from crapipy import AsyncClient


@pytest.mark.asyncio
async def test_profiles():
    client = AsyncClient()
    players = await client.get_players(['C0G20PR2', 'PY9VC98C'])
    assert players[0].name == 'SML'
    assert players[0].tag == 'C0G20PR2'
    assert players[0].clan.name == 'Reddit Bravo'
    assert players[0].clan.role.lower() == 'leader'
    assert players[1].name == 'Selfish'
    assert players[1].tag == 'PY9VC98C'
    assert players[1].clan.name == 'Reddit Gents.'
    assert players[1].clan.role.lower() == 'leader'
