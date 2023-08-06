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
import datetime
import typing

from league.enums import Queue, Season
from league.errors import EmptyResponse
from league.leagues import LeagueEntry, League
from league.mastery import ChampionMastery
from league.partial_match import PartialMatch
from league.riotDTO import RiotDto
from league.spectator import LiveMatch
from league.static_data import Champion


class Summoner(RiotDto):
    """Basic Representation of a League summoner.

    Attributes
    ----------
    id : int
        The :class:`Summoner`'s ID.

    name : str
        The :class:`Summoner`'s name.

    icon : int
        The ID of the :class:`Summoner`'s icon.

    level : int
        The level associated with the :class:`Summoner`.

    revision_date : `datetime.datetime`
        When the :class:`Summoner`'s profile was last modified in UTC.

    account_id : int
        The :class:`Summoner`'s account ID.

    region: :class:`Regions`
        The region the :class:`Summoner` belongs to.
    """

    def __init__(self, **kwargs):
        super(Summoner, self).__init__(**kwargs)
        self.id = kwargs.get('id', kwargs.get('summonerId', {}))
        self.name = kwargs.get('name', kwargs.get('summonerName', {}))
        self.icon = self._get_from_cache("profile_icons", kwargs.get('profileIconId', kwargs.get('profileIcon')))
        self.level = kwargs.get('summonerLevel')
        if kwargs.get('revisionDate'):
            date = kwargs.get('revisionDate') / 1000
            self.revision_date = datetime.datetime.utcfromtimestamp(date)
        else:
            self.revision_date = None
        self.account_id = kwargs.get('accountId')
        self.region = kwargs.get('region', kwargs.get('platformId', {}))

    def __eq__(self, other):
        if isinstance(other, Summoner):
            if self.id == getattr(other, "id"):
                return True
            elif self.account_id == getattr(other, "account_id"):
                return True
            else:
                return False

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name

    async def current_match(self) -> LiveMatch:
        """|coro|

        Get the :class:`Summoner`'s current match.

        Returns
        -------
        union[:class:`LiveMatch`, None]
            The live match of the :class:`Summoner` if found, otherwise returns ``None``.

        """
        endpoint = "active-games/by-summoner/{0}".format(self.id)
        try:
            data = await self._bucket.request("spectator", endpoint)
            if data is not None:
                return LiveMatch(**self._injector(data=data))
        except EmptyResponse:
            return None

    async def ranked_data(self) -> typing.List[LeagueEntry]:
        """|coro|

        Retrieves all :class:`LeagueEntry` data for all ranked queue types.

        Returns
        -------
        list[:class:`LeagueEntry`]
            All league data that the summoner belongs to.
        """
        endpoint = "positions/by-summoner/{0}".format(self.id)
        data = await self._bucket.request("league", endpoint)
        if data is not None:
            return sorted([LeagueEntry(**self._injector(data=league)) for league in data])
        else:
            return None

    async def champion_masteries(self) -> typing.List[ChampionMastery]:
        """|coro|

        Get all of the masteries for the specified :class:`Summoner`.

        Returns
        -------
        list[:class:`ChampionMastery`]
            A list of masteries for the specific :class:`Summoner`.
        """
        route = "champion-masteries/by-summoner/{0}".format(self.id)
        data = await self._bucket.request("champion-mastery", route)
        if data is not None:
            return sorted([
                ChampionMastery(summoner=self, champion=self._get_from_cache('champions', champ['championId']),
                                **self._injector(data=champ))
                for
                champ in data])

    async def champion_mastery(self, *, champion: typing.Union[Champion, int]) -> ChampionMastery:
        """|coro|

        Retrieves a mastery for a specified :class:`Champion`.

        Parameters
        ----------
        champion : Union[:class:`Champion`, int]
            The champion to lookup.

        Returns
        -------
        :class:`ChampionMastery`
            The mastery of the specified :class:`Champion`.
        """

        route = "champion-masteries/by-summoner/{0}/by-champion/{1}".format(self.id,
                                                                            getattr(champion, 'id') if hasattr(
                                                                                champion, 'id') else champion)
        data = await self._bucket.request("champion-mastery", route)
        if data is not None:
            return ChampionMastery(summoner=self, champion=champion, **self._injector(data=data))

    async def champion_mastery_score(self) -> int:
        """|coro|

        Retrieves the :class:`Summoner`'s total mastery score.

        Returns
        -------
        int
            :class:`Summoner`'s total mastery score.

        """
        route = "scores/by-summoner/{0}".format(self.id)
        data = await self._bucket.request("champion-mastery", route)
        if data is not None:
            return data

    async def recent_matches(self) -> typing.List[PartialMatch]:
        """|coro|

        Retrieves the last 20 matches for the :class:`Summoner`.

        Returns
        -------
        list[:class:`PartialMatch`]
            A list of the last 20 matches the :class:`Summoner` played.
        """
        route = "matchlists/by-account/{0}/recent".format(self.account_id)
        data = await self._bucket.request("match", route)
        if data is not None:
            formated_data = []
            for match in data['matches']:
                formated_data.append(PartialMatch(**self._injector(data=match)))
            return formated_data

    async def match_history(self) -> typing.List[PartialMatch]:
        """|coro|

        Alias for :func:`Summoner.recent_matches`

        """
        return await self.recent_matches()

    async def leagues(self) -> typing.List[League]:
        """|coro|

        Retrieves all the leagues the :class:`Summoner` belongs to across all queue types.

        Deprecated in 0.3.5

        Returns
        -------
        list : [:class:`League`]
            A list of all the ranked leagues this :class:`Summoner` belongs to.
        """
        raise DeprecationWarning("Endpoint depreciated, use client.get_league instead")
        # endpoint = "leagues/by-summoner/{0}".format(self.id)
        # data = await self._bucket.request("league", endpoint)
        # if data is not None:
        #     return [League(**self._injector(data=league)) for league in data]

    async def find_matches(self, begin_index: int = None, end_index: int = None,
                           queue: typing.List[typing.Union[Queue, int]] = None,
                           begin_time: datetime.datetime = None, end_time: datetime.datetime = None,
                           season: typing.List[typing.Union[Season, int]] = None,
                           champion: typing.List[typing.Union[Champion, int]] = None) -> typing.List[PartialMatch]:
        """

        Retrieves a :class:`PartialMatch` list result that can be filtered. All filters can be left blank.

        The max result given will be 50 matches

        Parameters
        ----------
        begin_index : Union[int,None]
            The begin index to use for filtering matchlist.
            If beginIndex is specified, but not endIndex, then endIndex defaults to beginIndex+50.
            If endIndex is specified, but not beginIndex, then beginIndex defaults to 0.
            If both are specified, then endIndex must be greater than beginIndex.
            The maximum range allowed is 50, otherwise a 400 error code is returned.
        end_index : Union[int,None]
            The end index to use for filtering matchlist. If beginIndex is specified,
            but not endIndex, then endIndex defaults to beginIndex+50.
            If endIndex is specified, but not beginIndex,
            then beginIndex defaults to 0. If both are specified,
            then endIndex must be greater than beginIndex.
            The maximum range allowed is 50, otherwise a 400 error code is returned.
        queue : list[Union[:class:`Queue`,int]]
            Set of queues of which to filter match_list
        begin_time : datetime
            If beginTime is specified, but not endTime, then these parameters are ignored.
            If endTime is specified, but not beginTime,
            then beginTime defaults to the start of the account's match history.
            If both are specified, then endTime should be greater than beginTime.
            The maximum time range allowed is one week, otherwise a 400 error code is returned.
        end_time : datetime
            If beginTime is specified, but not endTime, then these parameters are ignored. If endTime is specified,
            but not beginTime, then beginTime defaults to the start of the account's match history.
            If both are specified, then endTime should be greater than beginTime.
            The maximum time range allowed is one week, otherwise a 400 error code is returned.
        season : list[Union[:class:`Season`,int]]
            list of seasons to filter through.
        champion : list[Union[:class:`Champion`,int]]
            list of champions to filter through.
        Returns
        -------
        list : [:class:`PartialMatch`]
            A list of all matches that match the filter.

        """
        end_point = "matchlists/by-account/{0}".format(self.account_id)
        data = await self._bucket.request(
            "match",
            end_point,
            endIndex=end_index,
            queue=queue,
            endTime=end_time.timestamp() or None,
            beginTime=begin_time.timestamp() or None,
            season=season,
            champion=champion,
            beginIndex=begin_index
        )
        if data is not None:
            return [PartialMatch(**self._injector(match)) for match in data['matches']]
