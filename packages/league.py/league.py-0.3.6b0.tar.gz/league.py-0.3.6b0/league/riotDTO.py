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
from league.http import Bucket
import importlib
import typing
from league.enums import for_id


class RiotDto:
    """

    Attributes
    ----------
    raw_response : dict
        The raw response for the obj returned by the API.
    timestamp : datetime.datetime
        The UTC timestamp when this object was created.


    """

    def __init__(self, **kwargs):
        self._bucket = kwargs.get('bucket')  # type: Bucket
        self._static_cache = kwargs.get('cache')  # type: dict
        self._injector = kwargs.get('injector')  # type: typing.Callable
        self.raw_response = kwargs.get('raw_response')  # type: dict
        self._ranked_values = {"challenger": 100, "master": 90, "diamond": 80, "platinum": 70, "gold": 60, "silver": 50,
                               "bronze": 40,
                               "unranked": 0, "V": 5, "IV": 4, "III": 3, "II": 2, "I": 1}
        self.timestamp = datetime.datetime.utcnow()
        try:
            self._data_dragon_url = self._static_cache['versions'][0]
        except KeyError:
            self._data_dragon_url = None

    @staticmethod
    def _for_id(_id):
        return for_id(_id)

    @staticmethod
    def _get_object(wanted_obj: str, data: dict = None) -> typing.Union[object, None]:
        if data is None:
            return None
        my_class = getattr(importlib.import_module("league"), wanted_obj)
        if my_class is None:
            return None
        return my_class(**data)

    def _get_from_cache(self, cache: str,
                        item_id: typing.Union[int, str, typing.List[typing.Union[int, str]]]) -> typing.Any:
        if cache in self._static_cache:
            if isinstance(item_id, list):
                if len(self._static_cache.get(cache)) > 0:
                    return [self._static_cache.get(cache).get(item, item) for item in item_id]
            if len(self._static_cache.get(cache)) > 0:
                return self._static_cache.get(cache).get(item_id, item_id)
            else:
                return item_id
        else:
            return item_id

    def _injector(self, data):
        return self._injector(bucket=self._bucket, data=data)

    def _total_ranked_value(self, entry):
        return self._ranked_values[entry.rank] + self._ranked_values[entry.tier.lower()]
