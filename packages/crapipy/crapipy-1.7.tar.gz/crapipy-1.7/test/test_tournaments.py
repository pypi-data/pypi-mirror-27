import pytest

from crapipy import AsyncClient, Client


def assert_tournament_model(tournament):
    assert tournament.tag == '20LLGRLC'
    assert tournament.name == 'Reddit Alpha Clan Family'
    assert tournament.max_capacity == 50
    assert tournament.preparation_duration == 7200
    assert tournament.duration == 3600
    assert tournament.start_time == 1514505055
    assert tournament.create_time == 1514504131
    assert tournament.creator.tag == 'C0G20PR2'
    assert tournament.creator.name == 'SML'
    assert len(tournament.members) > 0


@pytest.mark.asyncio
async def test_tournament_async():
    client = AsyncClient()
    player = await client.get_tournament('20LLGRLC')
    assert_tournament_model(player)


def test_tournament():
    client = Client()
    player = client.get_tournament('20LLGRLC')
    assert_tournament_model(player)


