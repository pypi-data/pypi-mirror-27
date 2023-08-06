'''
MIT License

Copyright (c) 2017 grokkers

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
'''

import aiohttp
import requests
import asyncio
import requests
from .models import Player, Clan
from .errors import RequestError, NotFoundError, ServerError, NotResponding

class Client:

    '''Represents an async client connection to cr-api.com

    Attributes
    ----------
    session:
        The aiohttp ClientSession to be used for requests
    '''


    def __init__(self, token, session=None, timeout=10, is_async=False, camel_case=False):
        self.base = 'http://api.cr-api.com'
        self.token = token
        self.is_async = is_async
        self.timeout = timeout
        self.session = session or (aiohttp.ClientSession() if is_async else requests.Session())
        self.camel_case = camel_case
        self.headers = {
            'auth': token,
            'user-agent': 'Clash-Royale-Python'
            }

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        self.session.close()
    
    def __repr__(self):
        return f'<ClashRoyaleClient async={self.is_async}>'

    def close(self):
        self.session.close()
    
    def request(self, url):
        if self.is_async:
            return self._async_request(url)
        try:
            resp = self.session.get(url, timeout=self.timeout, headers=self.headers)
        except requests.Timeout:
            raise ServerError(resp, {})
        
        data = resp.json()
        # Request was successful 
        if resp.ok:
            return data

        # Tag not found
        if resp.status_code == 404:
            raise NotFoundError(resp, data)

        # Something wrong with the api servers :(
        if resp.status_code > 500:
            raise ServerError(resp, data)

        # Everything else
        else:
            raise RequestError(resp, data)

    async def _async_request(self, url):
        try:
            async with self.session.get(url, timeout=self.timeout, headers=self.headers) as resp:
                try:
                    data = await resp.json()
                except (asyncio.TimeoutError, aiohttp.ClientResponseError):
                    raise ServerError(resp, {})

                # Request was successful 
                if 300 > resp.status >= 200:
                    return data

                # Tag not found
                if resp.status == 404:
                    raise NotFoundError(resp, data)

                # Something wrong with the api servers :(
                if resp.status > 500:
                    raise ServerError(resp, data)

                # Everything else
                else:
                    raise RequestError(resp, data)
        except asyncio.TimeoutError:
            raise NotResponding()


    async def _aget_model(self, url, model):
        data = await self.request(url)

        if isinstance(data, list):
            return [model(self, c) for c in data]
        else:
            return model(self, data)

    def _get_model(self, url, model):
        if self.is_async:
            return self._aget_model(url, model)

        data = self.request(url)

        if isinstance(data, list):
            return [model(self, c) for c in data]
        else:
            return model(self, data)

    def get_player(self, *tags):
        '''Get player objects object using tag(s)'''
        url = '{0.base}/player/{1}'.format(self, ','.join(tags))
        return self._get_model(url, Player)

    get_players = get_player

    def get_clan(self, *tags):
        '''Get a clan object using tag(s)'''
        url = '{0.base}/clan/{1}'.format(self, ','.join(tags))
        return self._get_model(url, Clan)


    get_clans = get_clan

    # async def get_constants(self):
    #     '''Get clash royale constants.'''
    #     url = self.BASE + '/constants'

    #     data = await self.request(url)

    #     return Constants(self, data)

    # async def get_top_clans(self):
    #     '''Get a list of top clans, info is only brief, 
    #     call get_clan() on each of the ClanInfo objects 
    #     to get full clan info'''
    #     url = self.BASE + '/top/clans'

    #     data = await self.request(url)

    #     return [ClanInfo(self, c) for c in data.get('clans')]