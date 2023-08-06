League.py
-

[![Documentation Status](https://readthedocs.org/projects/leaguepy/badge/?version=latest)](http://leaguepy.readthedocs.io/en/latest/?badge=latest)
[![PyPI](https://img.shields.io/pypi/v/league.py.svg)](https://pypi.python.org/pypi/league.py/)
[![PyPI](https://img.shields.io/pypi/pyversions/league.py.svg)](https://pypi.python.org/pypi/league.py/)

### An Asyncio league of legends API wrapper made for python 3.5+


Built for Riot's new **V3** endpoints.

# Requirements

- Python 3.5+
- `aiohttp` library


# Installation
```
python3 -m pip install -U git+https://github.com/datmellow/League.py
```


# Example

```python
import league
import asyncio


async def test_method():
    client = league.Client(api_key="Token")
    await client.cache_setup() # Optional
    
    summoner = await client.get_summoner(summoner_name="RiotPhreak") # Gets a summoner
    print(summoner)
    current_match = await summoner.current_match() # Gets that summoner's current match if in one
    champion_masteries = await summoner.champion_masteries() # Gets all of their champion masteries
    
    vladimir = await client.get_champion_by_name(name="vladimir")
    if vladimir.ranked_enabled:
        print("Vladimir is allowed in ranked")
    if vladimir.free:
        print("Vladimir is free to play")


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(test_method())
```
you can see more indepth examples here: http://leaguepy.readthedocs.io/en/latest/quickstart.html
