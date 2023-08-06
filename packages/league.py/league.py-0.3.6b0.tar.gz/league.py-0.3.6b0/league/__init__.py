# -*- coding: utf-8 -*-

"""

An asyncio friendly wrapper for the Riot's League API.

:copyright: (c) 2017-2018 Datmellow
:license: MIT, see LICENSE for more details.

"""

__title__ = "league"
__author__ = "Datmellow"
__license__ = "MIT"
__copyright__ = "Copyright 2017-2018 Datmellow"
__version__ = "0.3.6b"

import logging
from collections import namedtuple
from league.summoner import Summoner
from league.leagues import League, LeagueEntry, Series
from league.mastery import ChampionMastery
from league.match import Player, TeamStats, Participant, Match, ParticipantTimeLine, ParticipantStats
from league.partial_match import PartialMatch
from league.errors import *
from league.client import Client
from league.enums import *
from league.static_data import Champion, RunePage, Rune, Item, SummonerMastery, Map, Image, Spell, Recommended, \
    ChampionStats,MasteryPage
from league.spectator import LiveMatch, LiveMatchParticipant
from league.riotDTO import RiotDto
from league.http import Statistics

VersionInfo = namedtuple('VersionInfo', 'major minor micro releaselevel serial')

version_info = VersionInfo(major=0, minor=3, micro=6, releaselevel='beta', serial=0)

try:
    from logging import NullHandler
except ImportError:
    class NullHandler(logging.Handler):
        def emit(self, record):
            pass

logging.getLogger(__name__).addHandler(NullHandler())
