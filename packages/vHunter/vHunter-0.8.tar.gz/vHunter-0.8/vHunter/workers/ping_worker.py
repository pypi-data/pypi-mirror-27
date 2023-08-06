import asyncio
import socket
import aiohttp
import logging

from utils import async_every


class PingWorker:
    def __init__(self, master_host, master_port):
        self.hostname = socket.gethostname()
        self.url = "http://{}:{}/ping/{}".format(master_host, master_port, self.hostname)
        self.ioloop = asyncio.get_event_loop()
        self.ioloop.call_soon(asyncio.ensure_future, self.ping_master())

    @async_every(seconds=10)
    async def ping_master(self):
        async with aiohttp.ClientSession() as session:
            async with session.post(self.url):
                logging.info("master has been pinged")
