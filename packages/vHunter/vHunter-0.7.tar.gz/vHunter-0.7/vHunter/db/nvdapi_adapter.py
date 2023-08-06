import aiohttp
import async_timeout
import logging
from pprint import pformat

from vHunter.db import BasicDbAdapter
from vHunter.utils import Config


class NvdapiAdapter(BasicDbAdapter):
    def __init__(self, min_score=5.0, max_pages=5):
        config = Config()['nvdapi']
        self.api_url = config['url']
        self.api_port = config['port']
        self.api_resource = config['resource']
        self.min_score = min_score
        self.max_pages = max_pages

    def prepare_request(self):
        return "{domain}:{port}{resource}".format(
            domain=self.api_url,
            port=self.api_port,
            resource=self.api_resource
        )

    def prepare_payload(self, thing, version=None, vendor=None):
        payload = {"product": thing}
        if version is not None:
            payload["version"] = version
        if vendor is not None:
            payload["vendor"] = vendor
        return payload

    async def check(self, thing, version=None, vendor=None):
        url = self.prepare_request()
        payload = self.prepare_payload(thing, version, vendor)
        grouped_results = []
        async with aiohttp.ClientSession() as session:
            logging.debug("will do the request with session: %s", session)
            counter = 0
            while True:
                if counter > self.max_pages:
                    logging.warning("Tried to fetch %s page with cve entries for %s, aborting. \nThis settings can be changed by passing max_pages parameter to NvdapiAdapter", counter, thing)
                    break
                with async_timeout.timeout(10):
                    async with session.get(url, params=payload) as response:
                        logging.debug("trying response: %s", response)
                        stuff = await response.json()
                        grouped_results = grouped_results + [vuln for vuln in stuff['results'] if vuln['score'] > self.min_score]
                        if stuff['next'] is None:
                            break
                    counter = counter + 1
        logging.debug("got responses: %s", pformat(grouped_results))
        return grouped_results
