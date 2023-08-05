from typing import Any, Optional, List, Coroutine, Union
import abc
import itertools
import logging
import asyncio
from asyncio.coroutines import _COROUTINE_TYPES
from asyncio.queues import Queue

import aiohttp
from aiohttp.client_reqrep import ClientResponse
from yarl import URL

from .pipelines import Pipeline, ThingProcessError
from .things import Request, Response, Item, Things


class Ant(abc.ABC):
    response_pipelines = [Pipeline()]  # type: List[Pipeline]
    request_pipelines = [Pipeline()]  # type: List[Pipeline]
    item_pipelines = [Pipeline()]  # type: List[Pipeline]

    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        # for background coroutines
        self.__queue = Queue()
        self.__count = 0

    async def request(self, url: Union[str, URL], method='GET', params: Optional[dict]=None, headers: Optional[dict]=None,
                      cookies: Optional[dict]=None, data: Optional[Any]=None,
                      proxy: Optional[str]=None) -> Response:
        self.logger.debug('{:s} {:s}'.format(method, str(url)))
        kwargs = locals()
        kwargs.pop('self')

        req = Request(**kwargs)
        req = await self._handle_thing_with_pipelines(req, self.request_pipelines)

        res = await self._request(req)

        res = await self._handle_thing_with_pipelines(res, self.response_pipelines)
        return res

    async def collect(self, item: Item) -> None:
        self.logger.debug('Collect item: ' + str(item))
        await self._handle_thing_with_pipelines(item, self.item_pipelines)

    async def open(self):
        self.logger.info('Opening')
        for pipeline in itertools.chain(self.item_pipelines, self.response_pipelines, self.request_pipelines):
            obj = pipeline.on_spider_open(self)
            if isinstance(obj, Coroutine):
                await obj

    async def close(self):
        for pipeline in itertools.chain(self.item_pipelines, self.response_pipelines, self.request_pipelines):
            obj = pipeline.on_spider_close(self)
            if isinstance(obj, Coroutine):
                await obj
        self.logger.info('Closed')

    @abc.abstractmethod
    async def run(self):
        """App custom entrance"""

    async def main(self):
        try:
            await self.open()
            await self.run()
            await self.__run_until_complete()
            await self.close()
        except Exception as e:
            self.logger.exception('Run main coroutine with ' + e.__class__.__name__)

    def ensure_future(self, coro_or_future: _COROUTINE_TYPES):
        self.__count += 1

        def _done_callback(f):
            self.__queue.put_nowait(f)

        asyncio.ensure_future(coro_or_future).add_done_callback(_done_callback)

    async def __run_until_complete(self):
        done_count = 0
        while done_count != self.__count:
            await self.__queue.get()
            done_count += 1

    async def _handle_thing_with_pipelines(self, thing: Things, pipelines: List[Pipeline]) -> Optional[Things]:
        """Process thing one by one, break the process chain when get None
        :raise ThingProcessError"""
        self.logger.debug('Process thing: ' + str(thing))
        raw_thing = thing
        for pipeline in pipelines:
            thing = pipeline.process(self, thing)
            if isinstance(thing, Coroutine):
                thing = await thing
            if thing is None:
                raise ThingProcessError(
                    'The thing {:s} is dropped because pipeline: {:s}'.format(str(raw_thing),
                                                                              pipeline.__class__.__name__))
        return thing

    async def _request(self, req: Request) -> Response:
        kwargs = {k: getattr(req, k) for k in req.__slots__}
        cookies = kwargs.pop('cookies')
        async with aiohttp.ClientSession(cookies=cookies) as session:
            async with session.request(**kwargs) as aio_response:
                await aio_response.read()
        return self._convert_response(aio_response, req)

    def _convert_response(self, aio_response: ClientResponse, request: Request) -> Response:
        return Response(request, aio_response.status, aio_response._content,
                        headers=aio_response.headers, cookies=aio_response.cookies,
                        encoding=aio_response._get_encoding())
