import logging
import asyncio
import time

from vHunter.utils import Config
from vHunter.utils import async_every
from vHunter.utils import Scenarios

from vHunter.drivers import *  # noqa: F401,F403


class ScenarioWorker:
    def __init__(self):
        self.config = Config()
        self.counter = 0
        self._running = False
        self.scenario_runs = {name: -1 for name in Scenarios()}
        logging.info("Scenario worker started")
        self.ioloop = asyncio.get_event_loop()
        self.ioloop.call_soon(asyncio.ensure_future, self.run())

    def load_driver(self, name, scenario, scenario_name):
        return globals()[name](scenario_name, scenario)

    @async_every(minutes=1)
    async def run(self):
        if self._running is True:
            logging.info("Scenario worker is still working on last course, waiting")
            return
        self._running = True
        drivers = []
        logging.info("Scenario worker running for %s time!", self.counter)
        scenarios = Scenarios()
        for name in scenarios:
            if time.time() - self.scenario_runs[name] > scenarios[name]['how_often'] * 60:
                logging.info("Performing %s", name)
                self.scenario_runs[name] = time.time()
                driver = self.load_driver(scenarios[name]['driver'], scenarios[name], name)
                drivers.append(driver.perform())
            else:
                logging.info(
                    "%s performed recently, skipping. Next run in: %6.2f minutes",
                    name,
                    scenarios[name]['how_often'] - (time.time() - self.scenario_runs[name]) / 60.0
                )
        self.counter = self.counter + 1
        for driver in drivers:
            await driver
        logging.info("Done performing %s scenarios, setting flag to idle", len(drivers))
        self._running = False
