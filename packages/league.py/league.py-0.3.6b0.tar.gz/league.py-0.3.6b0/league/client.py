# -*- coding: utf-8 -*-

"""
The MIT License (MIT)

Copyright (c) 2017 Datmellow

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
import asyncio
import copy
import logging

import aiohttp
import typing
from difflib import SequenceMatcher

from league.enums import *
from league.http import Bucket
from league.leagues import League, LeagueEntry
from league.match import Match
from league.partial_match import PartialMatch
from league.static_data import Champion, Rune, Item, Map, SummonerMastery, Image, Spell, SummonerSpell
from league.status import Shard
from league.summoner import Summoner
from league import errors
from league.errors import ServiceUnavailable

log = logging.getLogger(__name__)


class Client:
    """Represents the main client of league.py.

    .. _client session: http://aiohttp.readthedocs.io/en/stable/client_reference.html#aiohttp.ClientSession

    Parameters
    ----------
    api_key : str
        The API key for accessing riot's servers.

    session : Optional[client session]
        the `client session`_ to use for web operations. Defaults to ``None``,
        in which case a ClientSession is created.


    """

    def __init__(self, api_key: str, *, session: aiohttp.ClientSession = None,
                 static_cache: typing.Dict = None):

        self._session = aiohttp.ClientSession() if session is None else session  # type: aiohttp.ClientSession
        self._buckets = {item.name: Bucket(item.value, self._session, api_key) for item in
                         Regions}  # type: typing.Dict[str,Bucket]
        self.static_cache = static_cache if static_cache \
                                            is not None else {}  # type: typing.Dict[str,typing.Dict[int,object]]
        self._ready = asyncio.Event()
        self.cache_loaded = False

    async def wait_until_ready(self):
        await self._ready.wait()

    async def cache_setup(self, *, locale: str = "en_US", return_raw: bool = False) -> typing.Dict:
        """|coro|

        Parameters
        ----------
        locale : str
            The locale (language) to use for building the cache.
        return_raw : bool = False
            instead of setting up the cache, will return all the json responses. **Note**: This will not load the cache
            internally, this is only used for getting the responses by the module user to store themselves.


        Returns
        -------
        dict
            The static cache.

        """
        raw_data = {}
        for item in ['versions', 'champions', 'runes', 'items', 'maps', 'masteries', 'profile_icons',
                     'summoner_spells']:
            if item not in self.static_cache:
                for region in Regions:
                    try:
                        func = getattr(self, "get_all_{}".format(item))
                        if func is not None:
                            data = await func(region=region, locale=locale, return_raw=return_raw)
                            if return_raw:
                                raw_data[item] = data
                                break
                            elif data is not None:
                                self.static_cache[item] = data
                                break
                            else:
                                break
                        else:
                            break
                    except errors.ServiceUnavailable:
                        continue
                    except errors.UnAuthorized:
                        return {}
                    except errors.RateLimited:
                        continue
        if not return_raw:
            self._ready.set()
            self.cache_loaded = True
            return self.static_cache
        return raw_data

    def _data_injector(self, bucket: Bucket = None, data=None):
        """Func used for injecting additional data into objects.

        Parameters
        ----------
        bucket : :class:.Bucket
            The requests respective bucket, Can be None in certain circumstances.
        data : dict
            The response JSON dict.

        Returns
        -------
        dict
            Updated dictionary with all the new data added.

        """
        # Creates a copy
        new_data = copy.copy(data)
        # Adds bucket and data
        new_data['bucket'] = bucket
        new_data['raw_response'] = data
        # Checks if the respective obj have static_cache or _static_cache attribute, used for
        # compatibility regardless of where this function is called from.
        if hasattr(self, 'static_cache'):
            new_data['cache'] = self.static_cache
        elif hasattr(self, '_static_cache'):
            new_data['cache'] = getattr(self, "_static_cache")
        if hasattr(self, '_data_injector'):
            new_data['injector'] = self._data_injector
        elif hasattr(self, "_injector"):
            new_data['injector'] = getattr(self, "_injector")
        return new_data

    def __del__(self):
        if not self._session.closed:
            if asyncio.iscoroutinefunction(self._session.close):
                asyncio.ensure_future(self._session.close())
            else:
                self._session.close()

    async def get_summoner(self, *, summoner_id: int = None, summoner_name: str = None, account_id: int = None,
                           region: Regions = Regions.na) -> Summoner:
        """|coro|

        Searches for a summoner based on any given input, the order of parameters is based on the search order.


        Parameters
        ----------
        summoner_id : int
            The ID of the summoner to lookup.
        summoner_name : str
            The summoner name to lookup.
        account_id : int
            The account ID of the summoner to lookup.
        region : :class:`Regions`
            The region to get the summoner from.

        Returns
        -------
        :class:`Summoner`
            The summoner associated with the parameters given.

        Raises
        ------
        :class:`NoSummonerFound`
            Indicates if the API didn't return any results.
        """
        base_route = "summoners"
        if account_id is not None:
            route = "{}/by-account/{}".format(base_route, account_id)
        elif summoner_id is not None:
            route = "{}/{}".format(base_route, summoner_id)
        elif summoner_name is not None:
            route = "{}/by-name/{}".format(base_route, summoner_name)
        else:
            raise ValueError("Incorrect value passed")
        bucket = self._buckets[region.name]
        try:
            data = await bucket.request("summoner", route)
            if data is not None:
                return Summoner(region=region, **self._data_injector(bucket=bucket, data=data))
        except errors.EmptyResponse:
            raise errors.NoSummonerFound

    async def get_match(self, *, match_id: typing.Union[int, PartialMatch],
                        region: Regions = Regions.na) -> Match:
        """|coro|

        Searches for a match using the matchID/region pair provided.

        Parameters
        ----------
        match_id : Union[int, :class:`PartialMatch`]
            The ID of the match to lookup.
        region : :class:`Regions`
            The region the match belongs too.

        Returns
        -------
        :class:`Match`
            The Match with the ID given.

        Raises
        ------
        :class:`NoMatchFound`
            Indicates if the API didn't return any results.
        """
        route = "matches/{}".format(
            getattr(match_id, "match_id") if hasattr(match_id, "match_id") else match_id)
        data = await self._buckets[region.name].request("match", route)
        if data is not None:
            return Match(**self._data_injector(self._buckets[region.name], data))

    async def get_league(self, *, league: typing.Union[League, LeagueEntry, str], region: Regions = Regions.na):
        """
        Returns a :class:`League` with the specified ID


        Parameters
        ----------
        league :  Union[:class:`League`,:class:`LeagueEntry`,str]
        region : :class:`Regions`

        Returns
        -------
        :class:`League`


        """
        endpoint = "leagues/{}".format(league.id if isinstance(league, (League, LeagueEntry)) else league)
        data = await self._buckets[region.name].request("league", endpoint)
        if data is not None:
            return League(**self._data_injector(self._buckets[region.name], data))

    async def get_match_timeline(self, *, match_id: typing.Union[int, Match, PartialMatch],
                                 region: Regions = Regions.na):
        """|coro|

        Parameters
        ----------
        match_id : Union[int, :class:`PartialMatch`,:class:`Match`]
            The ID of the match to lookup.
        region : :class:`Regions`
            The region the match belongs to.

        Returns
        -------

        """
        route = "timelines/by-match/{}".format(
            getattr(match_id, "match_id") if hasattr(match_id, "match_id") else match_id)
        data = await self._buckets[region.name].request("match", route)
        if data is not None:
            return PartialMatch(**self._data_injector(self._buckets[region.name], data))

    def get_requests_statistics(self, *, region: Regions = Regions.na) -> typing.Dict[
        str, int]:
        """
        Retrieves request statistics for a certain region used by the :class:`Client` thus far.

        Parameters
        ----------
        region : :class:`Regions`
            The region to lookup stats.

        Returns
        -------
        :class:`Statistics`

        """
        return self._buckets[region.name].statistics

    async def get_challenger(self, *, queue_type: Queue, region: Regions = Regions.na) -> League:
        """|coro|

        Gets the :class:`League` of the challenger league for the specified region.

        Parameters
        ----------
        queue_type : :class:`Queue`
            The queue type to get challenger league for.
        region : :class:`Regions`
            The Region to lookup challenger for.
        Returns
        -------
        :class:`League`
            A League that contains everyone in challenger league

        """
        route = "challengerleagues/by-queue/{}".format(queue_type.value)
        data = await self._buckets[region.name].request("league", route)
        if data is not None:
            return League(**self._data_injector(self._buckets[region.name], data))

    async def get_champion_by_name(self, *, name: str, ignore_cache: bool = False, region: Regions = Regions.na,
                                   locale: str = "en_US") -> Champion:
        """|coro|

        Gets the :class:`Champion` using the name given.

        Parameters
        ----------
        name : str
            The name of the champion you want to lookup.
        ignore_cache : Bool
            Tells the function to ignore the cache and request the data from the API.
        region : :class:`Regions`
            The region to get the call against.
        locale : str
            Locale code for returned data.

        Returns
        -------
        :class:`Champion`

        Raises
        ------
        ValueError
            Indicates if the API didn't return any champion data.

        """
        if not self.static_cache.get('champions') or ignore_cache:
            route = "champions"
            data = await self._buckets[region.name].request("static-data", route, dataById=True,
                                                            locale=locale,
                                                            tags="all")
            if data is not None:
                for cdata in data['data'].values():
                    match_ratio = SequenceMatcher(None, cdata.get("name", ""), name.lower()).ratio()
                    if match_ratio > 0.8 or name.lower() == cdata.get("name", ""):
                        route = "champions/{}".format(cdata['id'])
                        ddata = await self._buckets[region.name].request("platform", route)
                        if ddata is not None:
                            objdata = {}
                            objdata.update(cdata)
                            objdata.update(data)
                            objdata.update(ddata)
                            return Champion(**self._data_injector(self._buckets[region.name], objdata))
                        else:
                            return

            else:
                raise ValueError("Champion name not found")
        else:
            for champ in self.static_cache['champions'].values():
                if name.lower() == champ.name.lower():
                    return champ
            else:
                raise ValueError("Champion name not found")

    async def get_champion_by_id(self, *, id: int, ignore_cache: bool = False, region: Regions = Regions.na,
                                 locale: str = "en_US") -> Champion:
        """|coro|

        Gets the :class:`Champion` by the ID provided

        Parameters
        ----------
        id : int
            The Champion ID to lookup.
        ignore_cache : bool
            Tells the function to ignore the cache and request the data from the API.
        region : :class:`Regions`
            The region to get the call against.
        locale : str
            Locale code for returned data.


        Returns
        -------
        :class:`Champion`

        Raises
        ------
        ValueError
            Indicates if the API didn't return any champion data.

        """
        try:
            if not self.static_cache.get('champions') or ignore_cache:
                mydata = {}
                route = "champions/{}".format(id)
                data = await self._buckets[region.name].request("static-data", route, dataById=True,
                                                                locale=locale,
                                                                tags="all")
                if data is None:
                    raise ValueError("Champion id not found")
                mydata.update(data)
                route = "champions/{}".format(id)
                ddata = await self._buckets[Regions.na.name].request("platform", route)
                mydata.update(ddata)
                return Champion(**self._data_injector(self._buckets[region.name], mydata))
            else:
                data = self.static_cache['champions'].get(id)
                if data is not None:
                    return data
                else:
                    raise ValueError("Champion id not found")
        except errors.EmptyResponse:
            return None

    async def get_all_champions(self, *, ignore_cache=False, region: Regions = Regions.na,
                                locale: str = "en_US", return_raw: bool = False) -> typing.Dict[int, Champion]:
        """|coro|

        Retrives all the champions.

        Parameters
        ----------
        ignore_cache : bool = False
            Tells the function to ignore the cache and request the data from the API.
        region : :class:`Regions`
            The region to get the call against.
        return_raw : bool = False
            If True will return the raw json request
        locale : str
            Locale code for returned data.

        Returns
        -------
        dict : {champion_id : :class:`Champion`}
            Returns all champions in the game.
        """
        if not self.static_cache.get('champions') or ignore_cache:

            base_route = "champions"
            champions = []
            base_data = await self._buckets[region.name].request("platform", base_route)
            other_data = await self._buckets[region.name].request("static-data", base_route, dataById=True,
                                                                  locale=locale, tags="all")
            if all([base_data, other_data]):
                if return_raw:
                    return {**base_data, **other_data}
                for champ in base_data['champions']:
                    combined_data = {}
                    combined_data.update(champ)
                    combined_data.update(other_data['data'][str(champ['id'])])
                    champions.append(Champion(**self._data_injector(self._buckets[region.name], combined_data)))
                champ_data = {}
                for champion in champions:
                    champ_data[champion.id] = champion
                self.static_cache['champions'] = champ_data
                return champ_data
            else:
                raise ServiceUnavailable()
        else:
            return self.static_cache['champions']

    async def get_all_runes(self, *, ignore_cache: bool = False, region: Regions = Regions.na,
                            locale: str = "en_US", return_raw: bool = False) -> typing.Dict[int, Rune]:
        """|coro|

        Retrieves all the runes from the API.

        Parameters
        ----------
        ignore_cache : bool = False
            Tells the function to ignore the cache and request the data from the API.
        region : :class:`Regions` = Regions.na
            The region to get the call against.
        return_raw : bool = False
            If True will return the raw json request
        locale : str
            Locale code for returned data.

        Returns
        -------
        dict : {rune_id : :class:`Rune`}
        """
        if not self.static_cache.get('runes') or ignore_cache:
            base_data = await self._buckets[region.name].request("static-data", 'runes', locale=locale,
                                                                 tags='all')
            if base_data is not None:
                if return_raw:
                    return base_data
                response = {}
                for key, value in base_data['data'].items():
                    response[int(key)] = Rune(**self._data_injector(self._buckets[region.name], value))
                return response

        else:
            return self.static_cache['runes']

    async def get_rune_by_id(self, *, rune_id: int, ignore_cache: bool = False, region: Regions = Regions.na,
                             locale: str = "en_US") -> Rune:
        """|coro|

        Parameters
        ----------
        rune_id : int
            The id of the rune to lookup
        ignore_cache : Bool
            Tells the function to ignore the cache and request the data from the API.
        region : :class:`Regions`
            The region to get the call against.
        locale : str
            Locale code for returned data.

        Returns
        -------
        :class:`Rune`
        """
        try:
            if not self.static_cache.get('runes') or ignore_cache:
                base_data = await self._buckets[region.name].request("static-data", 'runes/{}'.format(rune_id),
                                                                     locale=locale, tags="all")
                if base_data is not None:
                    return Rune(**self._data_injector(self._buckets[region.name], base_data))

            else:
                return self.static_cache['runes'].get(rune_id)
        except errors.EmptyResponse:
            return None

    async def get_all_items(self, *, region: Regions = Regions.na, ignore_cache: bool = False,
                            locale: str = "en_US", return_raw: bool = False) -> typing.Dict[int, Item]:
        """|coro|

        Retrieves all the items from the API.

        Parameters
        ----------
        ignore_cache : bool
            Tells the function to ignore the cache and request the data from the API.
        region : :class:`Regions`
            The region to get the call against.
        return_raw : bool
            If True will return the raw json request
        locale : str
            Locale code for returned data.

        Returns
        -------
        dict : {item_id : :class:`Item`}
        """
        if not self.static_cache.get('items') or ignore_cache:
            base_data = await self._buckets[region.name].request("static-data", 'items', locale=locale,
                                                                 tags="all")
            if base_data is not None:
                if return_raw:
                    return base_data
                response = {}
                for key, value in base_data['data'].items():
                    response[int(key)] = Item(**self._data_injector(self._buckets[region.name], value))
                for item, value in response.items():
                    new_data = []
                    if value.builds_from is not None:
                        for p in value.builds_from:
                            new_data.append(response.get(int(p)))
                        value.builds_from = new_data
                    new_data.clear()
                    if value.builds_into is not None:
                        for p in value.builds_into:
                            new_data.append(response.get(int(p)))
                            value.builds_into = new_data
                return response
        else:
            return self.static_cache['items']

    async def get_item_by_id(self, *, item_id: int, region: Regions = Regions.na, ignore_cache: bool = False,
                             locale: str = "en_US") -> Item:
        """|coro|

        Get an item by its ID.

        Parameters
        ----------
        item_id : int
            The item's ID.
        ignore_cache : bool
            Tells the function to ignore the cache and request the data from the API.
        region : :class:`Regions`
            The region to get the call against.
        locale : str
            Locale code for returned data.

        Returns
        -------
        :class:`Item`
        """
        try:
            if not self.static_cache.get('items') or ignore_cache:

                base_data = await self._buckets[region.name].request("static-data", 'items/{}'.format(item_id),
                                                                     locale=locale, tags="all")
                if base_data is not None:
                    return Item(**self._data_injector(self._buckets[region.name], base_data))
            else:
                return self.static_cache['items'].get(item_id)
        except errors.EmptyResponse:
            return None

    async def get_item_by_name(self, *, name: str, region: Regions = Regions.na, ignore_cache: bool = False,
                               locale: str = "en_US") -> Item:
        """|coro|

        Get an item by its name.

        Parameters
        ----------
        name: str
            the name of the item to look for.
        ignore_cache : bool
            Tells the function to ignore the cache and request the data from the API.
        region : :class:`Regions`
            The region to get the call against.
        locale : str
            Locale code for returned data.

        Returns
        -------
        :class:`Item`
        """
        try:
            if not self.static_cache.get('items') or ignore_cache:
                base_data = await self._buckets[region.name].request("static-data", 'items', locale=locale,
                                                                     tags="all")
                if base_data is not None:
                    for key, value in base_data['data'].items():
                        item_name = value.get("name", "")
                        match_ratio = SequenceMatcher(None, item_name.lower(), name.lower()).ratio()
                        if match_ratio > 0.8:
                            return Item(**self._data_injector(self._buckets[region.name], value))

            else:
                for item in self.static_cache.get('items').values():
                    item_name = getattr(item, "name", "") if hasattr(item, 'name') else ""
                    match_ratio = SequenceMatcher(None, item_name.lower(), name.lower()).ratio()
                    if match_ratio > 0.8 or name.lower() == item_name.lower():
                        return item
        except errors.EmptyResponse:
            return None

    async def get_status(self, *, region: Regions = Regions.na) -> Shard:
        """|coro|

        Gets the shard status for a specific region.

        Parameters
        ----------
        region : :class:`Regions`
            The server shard to lookup.

        Returns
        -------
        :class:`Shard`
        """
        method = "status"
        endpoint = "shard-data"
        data = await self._buckets[region.name].request(method, endpoint)
        if data is not None:
            return Shard(**self._data_injector(self._buckets[region.name], data))

    async def get_all_maps(self, *, region: Regions = Regions.na, ignore_cache: bool = False,
                           locale: str = "en_US", return_raw: bool = False) -> typing.Dict[int, Map]:
        """|coro|

        Parameters
        ----------
        ignore_cache : bool
            Tells the function to ignore the cache and request the data from the API.
        region : :class:`Regions`
            The region to get the call against.
        return_raw : bool
            If True will return the raw json request
        locale : str
            Locale code for returned data.

        Returns
        -------
        dict : {map_id : :class:`Map`}
        """
        if not self.static_cache.get('maps') or ignore_cache:
            data = await self._buckets[region.name].request("static-data", "maps", locale=locale)
            if return_raw:
                return data
            if data is not None:
                maps = {}
                for m in data['data']:
                    obj = Map(**self._data_injector(self._buckets[region.name], data['data'][m]))
                    maps[m] = obj
                return maps

        else:
            return self.static_cache['maps']

    async def get_all_masteries(self, *, region: Regions = Regions.na, ignore_cache: bool = False,
                                locale: str = "en_US", return_raw: bool = False) -> typing.Dict[int, SummonerMastery]:
        """|coro|

        Parameters
        ----------
        ignore_cache : bool
            Tells the function to ignore the cache and request the data from the API.
        region : :class:`Regions`
            The region to get the call against.
        return_raw : bool
            If True will return the raw json request
        locale : str
            Locale code for returned data.

        Returns
        -------
        dict : {mastery_id : :class:`SummonerMastery`}

        """
        if not self.static_cache.get('masteries') or ignore_cache:
            data = await self._buckets[region.name].request("static-data", "masteries", locale=locale, tags='all')
            if data is not None:
                if return_raw:
                    return data
                masteries = {}
                for m in data['data']:
                    obj = SummonerMastery(**self._data_injector(self._buckets[region.name], data['data'][m]))
                    masteries[int(m)] = obj
                return masteries

        else:
            return self.static_cache['masteries']

    async def get_all_profile_icons(self, *, region: Regions = Regions.na, ignore_cache: bool = False,
                                    locale: str = "en_US", return_raw: bool = False) -> typing.Dict[int, Image]:
        """|coro|

        Parameters
        ----------
        ignore_cache : bool = False
            Tells the function to ignore the cache and request the data from the API.
        region : :class:`Regions`
            The region to get the call against.
        return_raw : bool = False
            if set to true, will return the raw json response
        locale : str
            Locale code for returned data.

        Returns
        -------
        dict : {icon_id : :class:`Image`}
        """
        if not self.static_cache.get('icons') or ignore_cache:
            data = await self._buckets[region.name].request("static-data", "profile-icons", locale=locale,
                                                            tags='all')
            if data is not None:
                if return_raw:
                    return data
                profile_icons = {}
                for icon in data['data']:
                    obj = Image(**self._data_injector(self._buckets[region.name], data['data'][icon]['image']))
                    profile_icons[int(icon)] = obj
                return profile_icons
        else:
            return self.static_cache['profile_icons']

    async def get_all_summoner_spells(self, *, region: Regions = Regions.na, ignore_cache: bool = False,
                                      locale: str = "en_US", return_raw: bool = False) -> typing.Dict[
        int, SummonerSpell]:
        """|coro|

        Returns all summoner Spells

        Parameters
        ----------
        ignore_cache : bool
            Tells the function to ignore the cache and request the data from the API.
        region : :class:`Regions`
            The region to get the call against.
        return_raw : bool = False
            If set to true will return the raw json response
        locale : str
            Locale code for returned data.

        Returns
        -------
        dict : {spell_id : :class:`Spell`}
        """
        if not self.static_cache.get('summoner_spells') or ignore_cache:
            data = await self._buckets[region.name].request("static-data", "summoner-spells", locale=locale,
                                                            tags='all')
            if data is not None:
                if return_raw:
                    return data
                summoner_spells = {}
                for spell in data['data'].values():
                    obj = SummonerSpell(**self._data_injector(self._buckets[region.name], spell))
                    summoner_spells[int(spell['id'])] = obj
                return summoner_spells
        else:
            return self.static_cache['summoner-spells']

    async def get_summoner_spell_by_id(self, *, summoner_spell: int, region: Regions = Regions.na,
                                       ignore_cache: bool = False,
                                       locale: str = "en_US") -> SummonerSpell:
        """|coro|

        Get an item by its ID.

        Parameters
        ----------
        summoner_spell : int
            The spell's ID.
        ignore_cache : bool
            Tells the function to ignore the cache and request the data from the API.
        region : :class:`Regions`
            The region to get the call against.
        locale : str
            Locale code for returned data.

        Returns
        -------
        :class:`Item`
        """
        if not self.static_cache.get('summoner_spells') or ignore_cache:

            base_data = await self._buckets[region.name].request("static-data",
                                                                 'summoner-spells/{}'.format(summoner_spell),
                                                                 locale=locale, tags="all")
            if base_data is not None:
                return SummonerSpell(**self._data_injector(self._buckets[region.name], base_data))
        else:
            return self.static_cache['summoner_spells'].get(summoner_spell)

    async def get_all_versions(self, region: Regions.na, ignore_cache=False, locale: str = "en_US",
                               return_raw: bool = False):
        """
        Retrieves all the version data for the region

        Parameters
        ----------
        region: class:`Region`
        ignore_cache : bool
            Tells the function to ignore the cache and request the data from the API.

        Returns
        -------
        list[str]
            all the versions in newest -> oldest order

        """
        if not self.static_cache.get('versions') or ignore_cache:
            base_data = await self._buckets[region.name].request("static-data", 'versions')
            if base_data is not None:
                return base_data

        else:
            return self.static_cache['versions']
