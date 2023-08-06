# crapipy

This is an async Python wrapper for [cr-api](http://github.com/cr-api/cr-api). See http://docs.cr-api.com for documentation on the expected fields.

## Installation

Install via pip:

```sh
pip install crapipy
```

## How to use

You can access data using blocking or async code. Internally, the wrapper uses the requests library for blocking code and the aiohttp library for async code.

To initiate a client for connection:

### Blocking

```python
from crapipy import Client
client = Client()
```

### Async

```python
from crapipy import AsyncClient
client = AsyncClient()
```

## Methods

Both the blocking and async client uses the same method names. 

```python
player = client.get_profile('C0G20PR2')
```

The object returned allow you to access the JSON returned as dict or dot notation.

- dict: `player['arena']['arenaID']`
- attribute as CamelCaseKeys: `player.arena.arenaID`
- attribute as snake_case_attributes: `player.arena.arena_id`

Additionally, you can use:

- `to_dict()`: to read as dictionary
- `to_json()`: to convert back into JSON
- `to_yaml()`: to convert into YAML

### get_clan(tag)

### get_clans(tags)

### get_profile(tag)

### get_profiles(tags)

### get_constants()


## Examples

### Non-Async

```python
from crapipy import Client

def main():
    client = Client()

    # get player profile
    player = client.get_profile('C0G20PR2')
    assert player.name == 'SML'
    assert player.tag == 'C0G20PR2'
    assert player.clan_name == 'Reddit Delta'
    assert player.clan_role == 'Leader'
    assert player.deck is not None
    assert player.shop_offers is not None

    # profile equality
    player1 = client.get_profile('C0G20PR2')
    player2 = client.get_profile('C0G20PR2')
    assert player1 == player2

    # profile inequaity
    player1 = client.get_profile('C0G20PR2')
    player2 = client.get_profile('PY9VC98C')
    assert player1 != player2

    # get clan
    clan = client.get_clan('2CCCP')
    assert clan.name == 'Reddit Alpha'
    assert clan.badge.key == 'A_Char_Rocket_02'

    # multiple clans
    clans = client.get_clans(['2CCCP', '2U2GGQJ'])
    assert clans[0].name == 'Reddit Alpha'
    assert clans[0].badge.key == 'A_Char_Rocket_02'
    assert clans[1].name == 'Reddit Bravo'
    assert clans[1].badge.key == 'A_Char_Rocket_02'

main()
```

### Async

```python
import asyncio
from crapipy import AsyncClient

async def main():
    client = AsyncClient()

    # get player profile
    player = await client.get_profile('C0G20PR2')
    assert player.name == 'SML'
    assert player.tag == 'C0G20PR2'
    assert player.clan_name == 'Reddit Delta'
    assert player.clan_role == 'Leader'
    assert player.deck is not None
    assert player.shop_offers is not None

    # profile equality
    player1 = await client.get_profile('C0G20PR2')
    player2 = await client.get_profile('C0G20PR2')
    assert player1 == player2

    # profile inequaity
    player1 = await client.get_profile('C0G20PR2')
    player2 = await client.get_profile('PY9VC98C')
    assert player1 != player2

    # get clan
    clan = await client.get_clan('2CCCP')
    assert clan.name == 'Reddit Alpha'
    assert clan.badge.key == 'A_Char_Rocket_02'

    # multiple clans
    clans = await client.get_clans(['2CCCP', '2U2GGQJ'])
    assert clans[0].name == 'Reddit Alpha'
    assert clans[0].badge.key == 'A_Char_Rocket_02'
    assert clans[1].name == 'Reddit Bravo'
    assert clans[1].badge.key == 'A_Char_Rocket_02'


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.close()

```


## Tests

This package uses [pytest-asyncio](https://github.com/pytest-dev/pytest-asyncio) for tests.

Run all tests:

```sh
pytest
```



