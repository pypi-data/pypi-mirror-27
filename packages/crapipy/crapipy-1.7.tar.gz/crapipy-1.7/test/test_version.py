import pytest

from crapipy import AsyncClient, Client


def assert_version(version):
    assert isinstance(version, str)


@pytest.mark.asyncio
async def test_version_async():
    client = AsyncClient()
    version = await client.get_version()
    assert_version(version)


def test_version():
    client = Client()
    version = client.get_version()
    assert_version(version)


