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
import aiohttp
import asyncio
import copy
import datetime
import logging
import typing
from collections import Counter

from league import __version__
from league import errors
from .enums import RouteVersions

log = logging.getLogger(__name__)


class RateLimitHandler:
    """Abstract handler for managing the many rate limits.

    Attributes
    ----------
    limits : list
        A list of all the Rate-Limits from the response headers in dict form.

        dict :
            max : int The maximum calls this endpoint can handle.
            per_interval : int How many seconds between resets.
            next_reset : datetime The next time this limit expires.
            amount : int The amount of calls requested so far.
            amount_left : int The amount of calls left before a 429 is returned.
    last_request : datetime
        The datetime representation of when this handler was last used.
    locked : asyncio.Event
        used for locking down this handler to prevent 429's.
    cool_down : int
        Only used if a 429 is hit, this becomes what ever was in the try-after header.
    """

    def __init__(self, headers: typing.Dict):
        """

        Parameters
        ----------
        headers : dict
            The aiohttp response headers
        """
        self.limits = self.rate_limit_extractor(headers)
        self.last_request = datetime.datetime.utcnow()
        self.locked = asyncio.Event()
        self.cool_down = 0

    @staticmethod
    def rate_limit_extractor(headers):
        """Function used for extracting the app-rate-limit headers.

        Response header example:
        X-App-Rate-Limit: 100:1,1000:10,60000:600,360000:3600

        Extracts the numbers to keep track of.


        Parameters
        ----------
        headers : dict

        Returns
        -------

        """
        limits = []
        # Checks if the header even exists
        response_headers_limit = [(headers.get('X-App-Rate-Limit'), headers.get("X-App-Rate-Limit-Count")),
                                  (headers.get('X-Method-Rate-Limit'), headers.get('X-Method-Rate-Limit-Count'))]
        for header_limit, header_count in response_headers_limit:
            if all([header_limit is None, header_count is None]):
                continue
            # splits the headers by comma
            limit_header = header_limit.split(",")
            limit_header_count = header_count.split(",")
            # loops through each of the sets (1:1)
            for l, c in zip(limit_header, limit_header_count):
                # Splits the set up via :
                max_calls_limit, per_second_limit = l.split(":")
                amount_requests, requests_limit = c.split(":")
                # Creates the dictionary for storing the data
                limit_dict = {
                    "max": (int(max_calls_limit) / 2 * int(per_second_limit)),
                    "per_interval": int(per_second_limit),
                    "next_reset": datetime.datetime.utcnow() + datetime.timedelta(seconds=int(per_second_limit)),
                    "amount": int(amount_requests),
                    "amount_left": int(amount_requests) - int(max_calls_limit)
                }
                limits.append(limit_dict)
            return limits

    async def cool_down_handler(self):
        """
        Handles locking and unlocking the Handler.

        Returns
        -------

        """
        self.locked.clear()
        await asyncio.sleep(self.cool_down)
        self.locked.set()

    async def processor(self):
        # Check the lock status
        await self.locked.wait()
        # Goes through all of the limits
        for limit in self.limits:
            # Checks if the current time is past the expiration date
            if self.last_request < limit['next_reset']:
                # Resets the dict counter to 0 with the new reset timer
                limit['next_reset'] = datetime.datetime.utcnow() + datetime.timedelta(seconds=limit['per_interval'])
                limit['amount'] = 0
            # Checks if the request amount is close to the limit
            elif limit['amount_left'] - 2 <= 1:
                # calculate remaining time till next refresh
                time_to_sleep = datetime.datetime.utcnow() - limit['next_reset']
                # adds a warning message to the log
                log.warning(" {0} limit reached - Waiting {1}".format(limit['amount'], time_to_sleep.total_seconds()))
                self.cool_down = time_to_sleep.total_seconds()
                # Sleeps till the reset timer has passed
                await  self.cool_down_handler()
                # Resets the counter and refresh timer
                limit['next_reset'] = datetime.datetime.utcnow() + datetime.timedelta(seconds=limit['per_interval'])
                limit['amount'] = 0
            else:
                limit['amount'] += 1
        # sets the last request to current time
        self.last_request = datetime.datetime.utcnow()
        return


class Statistics:
    """
    Represents a bucket statistics used for collecting monitoring useful stats.

    Attributes
    ----------
    requests : int
        Total amount of requests called since this bucket was created.
    endpoints : Counter
        dict counter with method as keys with the amount of requests that method has used.
    responses : Counter
        dict counter with response codes as keys with the amount of times this response code has been returned.


    """

    def __init__(self):
        self.requests = 0
        self.endpoints = Counter()
        self.responses = Counter()

    def new_request(self, method, response):
        """
        Counter method for incrementing the counters.

        Parameters
        ----------
        method : str
            The method this request was for.
        response : object
            The aiohttp response.

        Returns
        -------

        """
        self.requests += 1
        self.endpoints[method] += 1
        if response is not None:
            self.responses[response.status] += 1


class Bucket:
    """Represents an abstraction of region/method API usage tracking. Used to keep track of API limits."""

    def __init__(self, region: str, session: aiohttp.ClientSession, api_key: str):
        self.base = "https://{0}.api.riotgames.com/lol/".format(region)
        self.handlers = {}  # type: typing.Dict[str,RateLimitHandler]
        self._session = session  # type: aiohttp.ClientSession
        self._api_key = api_key  # type: typing.Text
        self.statistics = Statistics()

    @staticmethod
    def clean_params(data: typing.Dict):
        """

        Used for converting any bool types into str.

        Parameters
        ----------
        data : dict

        Returns
        -------
        dict

        """
        if len(data) == 0:
            return {}
        for k, v in data.items():
            if v is True:
                data[k] = "true"
            elif v is False:
                data[k] = "false"
        return data

    def route_builder(self, method, route):
        """
        Dynamically builds the full url using the data given.


        Parameters
        ----------
        method : str
            The method this request is for.
        route : str
            The endpoint with any data needed.

        Returns
        -------
        str
            The fully built url.

        """
        url = "{base}{method}/{version}/{route}".format(base=self.base, method=method,
                                                        version=RouteVersions[method.replace("-", "_")].value,
                                                        route=route)
        return url

    async def raw_request(self, url) -> dict:
        """
        Handles an aiohttp request, bypassing the standard request method.

        Parameters
        ----------
        url : str
            The request URL.

        Returns
        -------
        dict
            The response JSON.

        """
        response = await self._session.get(url)
        if response.status == 200:
            data = await response.json()
            return data

    async def error_handler(self, response: aiohttp.ClientResponse, method):
        """Called if the response's status is not 200.

        Raises the appropriate error to the status code.

        Parameters
        ----------
        response : dict
            The response obj, used for grabbing status/JSON.
        method
            The method this response was used with.

        Raises
        -------
        Any

        """
        error_message = None
        error_json = await response.json()
        if error_json is not None:
            error_message = error_json['status']['message']
        if response.status == 400:
            try:
                raise errors.BadRequest(error_json)
            except errors.BadRequest as e:
                log.error(e)
        elif response.status == 403:
            raise errors.UnAuthorized
        elif response.status == 404:
            raise errors.EmptyResponse(message=error_message)
        elif response.status == 422:
            raise errors.InactivePlayer
        elif response.status == 429:
            cooldown = int(response.headers.get("Retry-After"))
            log.error(" 429 - Rate limited for {0} seconds on method {1}".format(cooldown, method))
            self.handlers[method].cool_down = cooldown
            await self.handlers[method].cool_down_handler()
        elif response.status in [500, 502, 503, 504]:
            raise errors.ServiceUnavailable

    async def request(self, method: str, route: str, **kwargs) -> typing.Union[dict, None]:
        """

        Parameters
        ----------
        method : str
            The method of the request.
        route : str
            The endpoint of the API.
        kwargs : any
            any additional data to pass along to the API.

        Returns
        -------
        dict:
            The JSON response dict.

        """
        url = self.route_builder(method, route)
        for param, value in copy.copy(kwargs).items():
            if value is None:
                del kwargs[param]
        cleaned_params = self.clean_params(kwargs)
        method_obj = self.handlers.get(method)
        headers = {
            "X-Riot-Token": self._api_key,
            "User-Agent": "Using : League.py/{0}".format(
                __version__)
        }
        if method_obj is not None:
            await asyncio.wait_for(method_obj.processor(), timeout=None)
        log.info("Requesting data from endpoint - {0}".format(method))
        async with self._session.get(url, params=cleaned_params, headers=headers) as response:

            log.info("{0} - Response on Method {1}".format(response.status, method))
            self.statistics.new_request(method, response)
            if method_obj is None:
                self.handlers[method] = RateLimitHandler(response.headers)
                self.handlers[method].locked.set()
            else:
                method_obj.rate_limit_extractor(response.headers)
            if response.status == 200:
                data = await response.json()  # type: dict
                return data
            else:
                await self.error_handler(response, method)
