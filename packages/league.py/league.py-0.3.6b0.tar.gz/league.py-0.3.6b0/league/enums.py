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

"""
Some code taken from:
https://github.com/meraki-analytics/cassiopeia/blob/master/cassiopeia/type/core/common.py
"""

from enum import Enum


class Regions(Enum):
    """Represents all valid legal regions for the api

    Attributes
    ----------
    br
    eune
    euw
    jp
    kr
    lan
    las
    na
    oce
    tr
    ru
    pbe

    """
    br = "br1"
    eune = "eun1"
    euw = "euw1"
    jp = "jp1"
    kr = "kr"
    lan = "la1"
    las = "la2"
    na = 'na1'
    oce = "oc1"
    tr = "tr1"
    ru = "ru"
    pbe = "pbe1"


class DataDragon(Enum):
    """
    """
    __base_url__ = "http://ddragon.leagueoflegends.com/cdn/"
    __data_version__ = "7.21.1"

    profile_icons = "{0}/img/profileicon/{1}"
    champion_splash = "img/champion/splash/{0}_{1}.jpg"
    champion_loading = "img/champion/loading/{0}_{1}.jpg"
    champion_square = "{0}/img/champion/{1}"
    passive = "{0}/img/passive/{0}"
    champion_spell = "{0}/img/spell/{0}"
    summoner_spell = "{0}/img/spell/Summoner{0}"
    item = "{0}/img/item/{1}"
    summoner_mastery = "{0}/img/mastery/{1}"
    rune = "{0}/img/rune/{1}"
    sprite = "{0}/img/sprite/{1}"
    minimap = "6.8.1/img/map/{1}"
    score_bored = "5.5.1/img/ui/{0}"


class RouteVersions(Enum):
    """Represents current route versions.

    Used to make future route versions easier to manage throughout code.

    """
    champion_mastery = "v3"
    platform = "v3"
    league = "v3"
    static_data = "v3"
    status = "v3"
    masteries = "v3"
    match = "v3"
    runes = "v3"
    spectator = "v3"
    summoner = "v3"
    tournament_stub = "v3"
    tournament = 'v3'


class Queue:

    def __init__(self, map_id, game_type):
        self.map = self.get_map_by_id(map_id)
        self.type = game_type
        self._map_ids = {
            1: "Summer Summoners Rift",
            2: "Autumn Summoners Rift",
            3: "Proving Grounds",
            4: "Original Twisted treeline",
            8: "Crystal Scar",
            10: "Twisted Treeline",
            11: "Summoners Rift",
            12: "Howling Abyss",
            14: "Butchers Bridge",
            16: "Cosmic Ruins",
            18: "Valoran City Park",
            19: "Substructure 43"
        }

    def __repr__(self):
        return self.type

    def __str__(self):
        return str(self.type)

    def get_map_by_id(self, map_id):
        try:
            return self._map_ids[map_id]
        except:
            return map_id


queues = {
    0: Queue(1, "Custom"),
    70: Queue(1, "One for All"),
    72: Queue(12, "1v1 Snowdown Showdown"),
    73: Queue(12, "2v2 Snowdown Showdown"),
    75: Queue(11, "6v6 Hexakill"),
    76: Queue(11, "Utra Rapid Fire"),
    78: Queue(11, "Mirrored One for All"),
    83: Queue(11, "Co-op vs AI Ultra Rapid Fire"),
    96: Queue(8, "Ascension"),
    98: Queue(10, "TT 6v6 Hexakill"),
    100: Queue(14, "5v5 ARAM"),
    300: Queue(12, "King Poro"),
    310: Queue(11, "Nemesis"),
    313: Queue(11, "Black Market Brawler"),
    317: Queue(8, "Definitely Not Dominion"),
    318: Queue(11, "All random URF"),
    325: Queue(11, "All Random"),
    400: Queue(11, "5v5 Draft Pick"),
    420: Queue(11, "Ranked Solo"),
    430: Queue(11, "5v5 Blind Pick"),
    440: Queue(11, "5v5 Ranked Flex"),
    450: Queue(12, "5v5 Aram"),
    460: Queue(10, "3v3 Blind Pick"),
    470: Queue(10, "3v3 Ranked Flex"),
    600: Queue(11, "Blood Hunt Assassin"),
    610: Queue(11, "Dark Star"),
    800: Queue(10, "Co-op vs AI Intermediate Bots"),
    810: Queue(10, "Co-op vs AI Intro Bots"),
    820: Queue(10, "Co-op vs AI Beginner Bots"),
    830: Queue(11, "Co-op vs. AI Intro Bot"),
    840: Queue(11, "Co-op vs. AI Beginner Bot"),
    850: Queue(11, "Co-op vs. AI Intermediate Bot"),
    940: Queue(11, "Nexus Siege"),
    950: Queue(11, "Doom Bots /w difficulty voting"),
    960: Queue(11, "Doom Bots"),
    980: Queue(18, "Star Guardian Invasion: Normal"),
    990: Queue(18, "Star Guardian Invasion: Onslaught"),
    1000: Queue(19, "PROJECT: Hunters")
}


def for_id(id_):
    """

    Args:
        id_:

    Returns:

    """
    try:
        return queues[id_]
    except:
        return id_


class Tier(Enum):
    """
    """
    challenger = "CHALLENGER"
    master = "MASTER"
    diamond = "DIAMOND"
    platinum = "PLATINUM"
    gold = "GOLD"
    silver = "SILVER"
    bronze = "BRONZE"
    unranked = "UNRANKED"


class Division(Enum):
    """
    """
    one = "I"
    two = "II"
    three = "III"
    four = "IV"
    five = "V"


class Season(Enum):
    season_seven = 9
    pre_season_seven = 8
    season_six = 7
    pre_season_six = 6
    season_five = 5
    preseason_five = 4
    season_four = 3
    preseason_four = 2
    season_three = 1
    pre_season_three = 0


if __name__ == '__main__':
    pass
