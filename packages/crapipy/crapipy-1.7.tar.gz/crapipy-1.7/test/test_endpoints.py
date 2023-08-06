import pytest

from crapipy import AsyncClient, Client


def assert_endpoints(endpoints):
    assert len(endpoints) > 5


@pytest.mark.asyncio
async def test_endpoints_async():
    client = AsyncClient()
    endpoints = await client.get_endpoints()
    assert_endpoints(endpoints)


def test_endpoints():
    client = Client()
    endpoints = client.get_endpoints()
    assert_endpoints(endpoints)


